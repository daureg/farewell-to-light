#! /usr/bin/python2
# vim: set fileencoding=utf-8
"""Save number of checkins over a day or a week, in a city or globally."""
import os
import sys
import numpy as np
from functools import wraps
sys.path.insert(0, os.path.abspath('../../illalla'))


def add_symlink(func):
    """Create a symlink for the first argument of `func` in the parent
    directory."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        filename = args[0]
        if isinstance(filename, str):
            if not filename.endswith('.dat'):
                filename += '.dat'
            try:
                os.symlink(filename, os.path.join('..', filename))
            except OSError:
                pass
        return func(filename, *args[1:], **kwargs)
    return wrapper


@add_symlink
def save_data(filename, data, **kwargs):
    """Save `data` in `filename` as text file."""
    options = dict(comments='')
    options.update(kwargs)
    # pylint: disable=E1101
    np.savetxt(filename, data, **options)


def save_checkins_time(db, city=None, chunk=4):
    """Read checkin from `db` (potentially only in `city`) and save their
    daily and weekly distribution in two text files."""
    out_name = (city or 'global') + '_'
    query = {'city': city} if city else {}
    day, week = [], []
    nb_chunks = 24 / chunk
    for checkin in db.checkin.find(query, {'time': 1, '_id': 0}):
        time = checkin['time']
        day.append(time.hour)
        week.append(time.weekday()*nb_chunks + (time.hour % nb_chunks))
    nb_checkin = len(day)
    # pylint: disable=E1101
    day = np.bincount(day, minlength=24).astype(float)/nb_checkin
    save_data(out_name+'day.dat', np.array([np.arange(24), 100*day]).T,
              fmt='%d\t%.6f', header='time\tfreq',
              footer='# '+str(nb_checkin))
    week = np.bincount(week, minlength=7*nb_chunks).astype(float)/nb_checkin
    save_data(out_name+'week.dat',
              np.array([np.arange(7*nb_chunks), 100*week]).T,
              fmt='%d\t%.6f', header='time\tfreq', footer='# '+str(nb_checkin))


def save_time_cluster(week, shorter):
    import scipy.io as sio
    import cities
    # import VenueFeature as vf
    nbclass = 3 if week else 5
    size = 21 if week else (6 if shorter else 8)
    # pylint: disable=E1101
    dirname = '../../illalla/' + ('times/' if shorter else 'time/')
    suffix = '_' + ('weekly' if week else 'daily') + '_time.mat'
    out_name = '{{}}_cluster_{}_{}'.format('week' if week else 'day',
                                           '4h' if shorter else '3h')
    # ticks = np.array(vf.named_ticks('mix' if week else 'day',
    #                                 2 if shorter else 1,
    #                                 (4 if shorter else 3)))
    ticks = np.arange(size).astype(int)
    fmt = '%d\t' + '\t'.join(nbclass*['%.6f', ])
    for name in cities.SHORT_KEY:
        clusters = 100*sio.loadmat(dirname + name + suffix)['t'].T
        save_data(out_name.format(name), np.c_[ticks, clusters], fmt=fmt)

if __name__ == '__main__':
    # pylint: disable=C0103
    save_time_cluster(False, True)
    import CommonMongo as cm
    import arguments
    args = arguments.city_parser().parse_args()
    DB, CLIENT = cm.connect_to_db('foursquare', args.host, args.port)
    # save_checkins_time(DB, args.city)
    # save_checkins_time(DB)

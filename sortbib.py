#! /usr/bin/python
# vim: set fileencoding=utf-8
"""Maintain consistent order within a Mendeley exported .bib file"""
if __name__ == '__main__':
    with open('strip.bib') as f:
        bib = f.readlines()
    inbib = False
    save = []
    name = ''
    res = {}
    for line in bib:
        if line[0] == '@':
            if not inbib:
                name = line.strip()
                inbib = True
                continue
            res[name] = '\n'.join([name]+save)
            del save[:]
            name = line.strip()
            print(name)
        elif inbib:
            save.append(line.strip())
    res[name] = '\n'.join([name]+save)
    with open('nstrip.bib', 'w') as f:
        f.write('\n'.join((_[1] for _ in sorted(res.items()))))

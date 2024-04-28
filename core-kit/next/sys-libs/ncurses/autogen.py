#!/usr/bin/env python3

from bs4 import BeautifulSoup
from metatools.version import generic
import re

regex = r'(\d+(?:[\.-]\d+)+)'

async def generate(hub, **pkginfo):
    download_url="https://invisible-mirror.net/archives/ncurses/"
    html = await hub.pkgtools.fetch.get_page(download_url)
    soup = BeautifulSoup(html, 'html.parser').find_all('a', href=True)


    releases = [a for a in soup if 'ncurses' in a.contents[0] and not a.contents[0].endswith('asc')]
    latest = max([(
            generic.parse(re.findall(regex, a.contents[0])[0]),
            a.get('href'))
        for a in releases if re.findall(regex, a.contents[0])
    ])
    pkginfo['soname'] = latest[0].major

    stable_artifact = hub.pkgtools.ebuild.Artifact(url=download_url + latest[1])

    # Find all the patches
    patches_url = download_url + latest[0].public + '/'
    html = await hub.pkgtools.fetch.get_page(patches_url)
    soup = BeautifulSoup(html, 'html.parser').find_all('a', href=True)

    # Ignore the first patch, as that one is to upgrade from the previous major.minor version to this one
    patches = [(generic.parse(re.findall(regex, a.get('href'))[0]), a.get('href')) for a in soup if re.findall(regex, a.contents[0]) and not 'asc' in a.get('href')][1:]


    try:
        # Find the newest patch
        newest = max(patches)[0]
        version = latest[0].public + "_p" + str(newest.post)
    except ValueError:
        newest = None
        version = latest[0].public

    patch_artifacts = [hub.pkgtools.ebuild.Artifact(url=patches_url + p[1]) for p in patches]

    ebuild = hub.pkgtools.ebuild.BreezyBuild(
        **pkginfo,
        version=version,
        revision={'6.4_p20221231' : '1'},
        artifacts=[stable_artifact] + patch_artifacts,
        patches=[p[1].split('.gz')[0] for p in patches] # a list of all the unzipped patch filenames
    )
    ebuild.push()


#vim: ts=4 sw=4 noet

# Distributed under the terms of the GNU General Public License v2

EAPI=7

DESCRIPTION="A set of scripts and m4/autoconf macros that ease build system maintenance"
HOMEPAGE="https://www.xfce.org/ http://users.xfce.org/~benny/projects/xfce4-dev-tools/"
SRC_URI="https://archive.xfce.org/src/xfce/${PN}/${PV%.*}/${P}.tar.bz2"

LICENSE="GPL-2+"
SLOT="0"
KEYWORDS="*"
IUSE=""

RDEPEND=">=dev-libs/glib-2.42"
DEPEND="${RDEPEND}
	virtual/pkgconfig"

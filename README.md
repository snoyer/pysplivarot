# pysplivarot

A python module to compute boolean operations on SVG paths using [Inkscape][inkscape]'s algorithms.

![example](examples/generated/abc-7.svg)
![example](examples/generated/abc-8.svg)


(Using [lib2geom][lib2geom] would be a better alternative
but as of yet Inkscape seem to provide better results for boolean operations.)


## Example

~~~ python
import pysplivarot
a = pysplivarot.parse_svgd('M0,0 V2 H2 V0 z')
b = pysplivarot.parse_svgd('M1,1 V3 H3 V1 z')
print pysplivarot.format_svgd(a + b) # c = a union b
print pysplivarot.format_svgd(a - b) # d = a minus b
print pysplivarot.format_svgd(a * b) # d = a inter b
#  _____       _____       _____
# |a  __|__   |c    |__   |d  __|   __
# |__|__| b|  |___     |  |__|     |e_|
#    |_____|      |____|
#
~~~
~~~
M 0 0 V 2 H 1 V 3 H 3 V 1 H 2 V 0 z
M 0 0 V 2 H 1 V 1 H 2 V 0 z
M 1 1 V 2 H 2 V 1 z
~~~



## Prerequisites

The python modules depedns on :

- `livarot_LIB` and `2geom_LIB` from Inkscape build
- `fixlivarotlib` (compiled by `setup.py` to plug some missing symbols in `livarot_LIB`)
- `gsl`, `blas`, `cairo`, `glib-2.0` needed by Inkscape's code


Installing Inkscape dependencies (on Ubuntu) :
~~~sh
sudo apt-get install cmake pkg-config libgsl-dev libharfbuzz-dev libpango1.0-dev libgc-dev libpopt-dev libgdl-3-dev libgtkmm-3.0-dev libxslt1-dev libcairo2-dev libblas-dev libboost-dev libboost-python-dev
~~~

Minimal compilation of Inkscape modules (from source directory) :
~~~ sh
mkdir build
cd build
cmake .. -DBUILD_SHARED_LIBS=YES -DENABLE_LCMS=NO -DENABLE_BINRELOC=NO -DENABLE_POPPLER=NO -DENABLE_POPPLER_CAIRO=NO -DWITH_DBUS=NO -DWITH_GNOME_VFS=NO -DWITH_IMAGE_MAGICK=NO -DWITH_LIBCDR=NO -DWITH_LIBVISIO=NO -DWITH_LIBWPG=NO -DWITH_LPETOOL=NO -DWITH_NLS=NO -DWITH_OPENMP=NO -DWITH_PROFILING=NO -DWITH_SVG2=NO -DWITH_YAML=NO
make livarot_LIB 2geom_LIB
~~~

Compiling the module :
~~~ sh
pip install --upgrade .
~~~





[inkscape]: https://inkscape.org/
[lib2geom]: https://github.com/inkscape/lib2geom

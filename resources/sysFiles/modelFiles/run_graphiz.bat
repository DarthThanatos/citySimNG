rem Before running this script:

rem 1) download Microsoft Visual C++ Compiler 9.0 for Python 2.7 
rem    from https://www.microsoft.com/en-us/download/details.aspx?id=44266

rem 2) download graphviz-2.38.msi file from http://www.graphviz.org/Download_windows.php and during installation, 
rem    when asked, set instalation folder path to C:/Graphviz2.38

rem 3) Add C:/Graphviz2.38/bin to PATH environmental variable

python -m pip install pygraphviz ^
	--install-option="--include-path=C:/Graphviz2.38/include" ^
	--install-option="--library-path=C:/Graphviz2.38/lib/release/lib"
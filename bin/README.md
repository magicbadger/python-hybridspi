`xml_to_binary` turns an SI to a data directory with encoded binary SI and image data, along with a manifest
`encode_manifest` encodes the manifest into a directory bitstream. These libraries to do this are not currently publicly available.

``
./xml_to_binary -e e1.c1c8 SI.xml
./encode_manifest -p -o out data
``

you can decode the data using the python-msc decode script (again, not currently publicly available :(

``
python ~/git/python-msc/bin/decode.py -p -d -o -m mot.epg out
``

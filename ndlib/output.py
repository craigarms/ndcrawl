'File output routines'
import csv
import logging

logger = logging.getLogger(__name__)

def output_files(outf, ngout, dout, neighbors, devices, distances):
    """ Output files to CSV if requested """

    # Output Neighbor CSV File
    if outf:
        fieldnames = ['local_device_id', 'remote_device_id', 'distance', 'local_int',
                      'remote_int', 'ipv4', 'os', 'platform', 'description','version', 'image']
        f = open(outf, 'w', newline="\n")
        dw = csv.DictWriter(f, fieldnames=fieldnames)
        dw.writeheader()
        for n in neighbors:
            nw = n.copy()
            if 'logged_in' in nw:
                nw.pop('logged_in')
            dw.writerow(nw)
        f.close()

    # Output NetGrph CSV File
    if ngout:
        fieldnames = ['LocalName', 'LocalPort', 'RemoteName', 'RemotePort']
        f = open(ngout, 'w', newline="\n")
        dw = csv.DictWriter(f, fieldnames=fieldnames)
        dw.writeheader()
        for n in neighbors:

            ng = {'LocalName': n['local_device_id'].split('.')[0],
                  'LocalPort': n['local_int'],
                  'RemoteName': n['remote_device_id'].split('.')[0],
                  'RemotePort': n['remote_int'],
                 }
            dw.writerow(ng)
        f.close()

    if dout:
        fieldnames = ['device_id', 'ipv4', 'platform', 'os', 'version', 'image', 'logged_in']
        f = open(dout, 'w', newline="\n")
        dw = csv.DictWriter(f, fieldnames=fieldnames)
        dw.writeheader()
        for d in sorted(devices):
            logged_in = False
            if 'logged_in' in devices[d] and devices[d]['logged_in']:
                logged_in = True

            dd = {'device_id': devices[d]['remote_device_id'], 'ipv4': devices[d]['ipv4'],
                  'platform': devices[d]['platform'], 'os': devices[d]['os'],
                  'version' : devices[d]['version'], 'image': devices[d]['image'],
                  'logged_in': logged_in}
            dw.writerow(dd)

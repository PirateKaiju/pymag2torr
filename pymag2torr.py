import sys
import tempfile
import libtorrent as lt
from time import sleep
import shutil

#print(libtorrent.version)

#Creates a torrent file from a magnet link at current directory
def mag2torr(magnet):
    
    tempDir = tempfile.mkdtemp() #Directory to store temporary torrent metadata

    #For libtorrent use
    params = {
            'save_path': tempDir,
            'storage_mode': lt.storage_mode_t(2),
            'paused': False,
            'auto_managed': True,
            'duplicate_is_error': True
    }

    #Creates a session and a handle, to download data from torrent network
    sessionT = lt.session() 
    handle = lt.add_magnet_uri(sessionT, magnet, params)

    while (not handle.has_metadata()): #Wait for completion
        try:
            print("Downloading metadata...")
            sleep(1)
        except KeyboardInterrupt:
            print("Aborting...")
            sessionT.pause()
            sessionT.remove_torrent(handle)
            #shutil.rmtree(tempDir)
            sys.exit(0)
            
    sessionT.pause()
    print("Done")

    torrentInfo = handle.get_torrent_info()
    fileName = "m2t_" + torrentInfo.name() + ".torrent"
    print("Torrent name: " + torrentInfo.name())

    #Builds torrent file from downloaded metadata
    torrentFile = lt.create_torrent(torrentInfo)

    with open(fileName, "wb") as op:
        #It is necessary to encode for matching torrent file standards
        op.write(lt.bencode(torrentFile.generate()))

    #Cleanup
    sessionT.remove_torrent(handle)
    shutil.rmtree(tempDir)


if __name__ == "__main__":
    if(len(sys.argv) >= 2):
        #print(sys.argv[1])
        for magnet in sys.argv[1:] :
            mag2torr(magnet)
        print("Finished!")
    else:
        print("Please supply magnet as string argument!")

#TODO: Check for valid magnets
import os
import paramiko
import numpy
import pyfits
import warnings
import select

class VLTConnection( object ):
    """
    VLTConnection:  This object allows python to log into a computer
    running the VLT SPARTA Light software and do the following:
        - Send a new flat pattern to the DM
        - Retrieve data from the RTC (slopes, intensities, etc...)
        - what else?

    """
    def __init__(self, hostname, username, simulate = True):
        """
        hostname: - Name of the VLT workstation - string
        username: - Name of the CIAO user account - string
        simulate: - if True, simulate access to CDMS/SPARTA Light
                  - if False, send commands to CDMS/SPARTA Light
        """
        self.hostname = hostname
        self.username = username
        self.ssh = paramiko.SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.connect(self.hostname, username=self.username)
        self.ftp = self.ssh.open_sftp()
        self.localpath = './data/'
        self.remotepath = './local/test/'
        self.CDMS = CDMS()
        self.sim = simulate

    def simulate(self):
        """
        This routine sets the VLT communication into simulation mode
        """
        self.sim = True

    def goLive(self):
        """
        This routine takes the VLT communication out of simulation mode
        """
        self.sim = False

    def sendCommand(self, command):
        if not(self.sim):
            stdin, stdout, stderr = self.ssh.exec_command(command)
            while not stdout.channel.exit_status_ready():
                if stdout.channel.recv_ready():
                    rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
                    if len(rl) > 0:
                        print stdout.channel.recv(1024)
        else:
            print("VLT Connection in Simulation mode.  The command I would have sent is:")
            print(command)

    def set_new_HO_flat_map(self, pattern):
        self.CDMS.maps["HOCtr.ACT_POS_REF_MAP"].replace(pattern)
        self.CDMS.maps["HOCtr.ACT_POS_REF_MAP"].write(path=self.localpath)
        name = self.CDMS.maps["HOCtr.ACT_POS_REF_MAP"].outfile
        self.ftp.put(self.localpath+name, self.remotepath+name)
        #print "Put flat map on "+self.hostname
        #print "Applying flat map to CDMS"
        stdin, stdout, stderr = self.ssh.exec_command("cdmsLoad -f "+self.remotepath+name+" HOCtr.ACT_POS_REF_MAP --rename")
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
                if len(rl) > 0:
                    print stdout.channel.recv(1024)

    def set_new_TT_flat_map(self, pattern):
        self.CDMS.maps["TTCtr.ACT_POS_REF_MAP"].replace(pattern)
        self.CDMS.maps["TTCtr.ACT_POS_REF_MAP"].write(path=self.localpath)
        name = self.CDMS.maps["TTCtr.ACT_POS_REF_MAP"].outfile
        self.ftp.put(self.localpath+name, self.remotepath+name)
        stdin, stdout, stderr = self.ssh.exec_command("cdmsLoad -f "+self.remotepath+name+" TTCtr.ACT_POS_REF_MAP --rename")
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
                if len(rl) > 0:
                    print stdout.channel.recv(1024)

    def set_TT_gain(self, gain):
        self.sendCommand("msgSend \"\" CDMSGateway SETMAP \"-object TTCtr.TERM_B -function 0,0="+str("%.2g" % gain)+"\"")
        self.sendCommand("msgSend \"\" spaccsServer EXEC \"-command TTCtr.update ALL\"")

    def set_HO_gain(self, gain):
        self.sendCommand("msgSend \"\" CDMSGateway SETMAP \"-object HOCtr.TERM_B -function 0,0="+str("%.2g" % gain)+"\"")
        self.sendCommand("msgSend \"\" spaccsServer EXEC \"-command HOCtr.update ALL\"")

    def set_gain(self, gain):
        termA = numpy.array([-1], dtype='float32')
        termB = gain*(numpy.array([-1.0, 0.0], dtype='float32'))
        self.CDMS.maps["HOCtr.TERM_A"].replace(termA)
        self.CDMS.maps["HOCtr.TERM_B"].replace(termB)
        self.CDMS.maps["HOCtr.TERM_A"].write(path=self.localpath)
        self.CDMS.maps["HOCtr.TERM_B"].write(path=self.localpath)
        nameA = self.CDMS.maps["HOCtr.TERM_A"].outfile
        nameB = self.CDMS.maps["HOCtr.TERM_B"].outfile
        self.ftp.put(self.localpath+nameA, self.remotepath+nameA)
        self.ftp.put(self.localpath+nameB, self.remotepath+nameB)
        stdin, stdout, stderr = self.ssh.exec_command("cdmsLoad -f "+self.remotepath+nameA+" HOCtr.TERM_A --rename")
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
                if len(rl) > 0:
                    print stdout.channel.recv(1024)
        stdin, stdout, stderr = self.ssh.exec_command("cdmsLoad -f "+self.remotepath+nameB+" HOCtr.TERM_B --rename")
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
                if len(rl) > 0:
                    print stdout.channel.recv(1024)
        termB = gain*(numpy.array([-1.0, 0.0], dtype='float32'))
        self.CDMS.maps["TTCtr.TERM_A"].replace(termA)
        self.CDMS.maps["TTCtr.TERM_B"].replace(termB)
        self.CDMS.maps["TTCtr.TERM_A"].write(path=self.localpath)
        self.CDMS.maps["TTCtr.TERM_B"].write(path=self.localpath)
        nameA = self.CDMS.maps["TTCtr.TERM_A"].outfile
        nameB = self.CDMS.maps["TTCtr.TERM_B"].outfile
        self.ftp.put(self.localpath+nameA, self.remotepath+nameA)
        self.ftp.put(self.localpath+nameB, self.remotepath+nameB)
        stdin, stdout, stderr = self.ssh.exec_command("cdmsLoad -f "+self.remotepath+nameA+" TTCtr.TERM_A --rename")
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
                if len(rl) > 0:
                    print stdout.channel.recv(1024)
        stdin, stdout, stderr = self.ssh.exec_command("cdmsLoad -f "+self.remotepath+nameB+" TTCtr.TERM_B --rename")
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
                if len(rl) > 0:
                    print stdout.channel.recv(1024)

    def make_TT_unscr(self):
        self.CDMS.maps["TTCtr.SEC_ACT_UNSCR_MAP"].write(path=self.localpath)
        name = self.CDMS.maps["TTCtr.SEC_ACT_UNSCR_MAP"].outfile
        self.ftp.put(self.localpath+name, self.remotepath+name)
        stdin, stdout, stderr = self.ssh.exec_command("cdmsLoad -f "+self.remotepath+name+" TTCtr.SEC_ACT_UNSCR_MAP --rename")
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
                if len(rl) > 0:
                    print stdout.channel.recv(1024)

    def set_CommandMatrix(self, pattern):
        self.CDMS.maps["Recn.REC1.CM"].replace(pattern)
        self.CDMS.maps["Recn.REC1.CM"].write(path=self.localpath)
        name = self.CDMS.maps["Recn.REC1.CM"].outfile
        self.ftp.put(self.localpath+name, self.remotepath+name)
        stdin, stdout, stderr = self.ssh.exec_command("cdmsLoad -f "+self.remotepath+name+" Recn.REC1.CM --rename")
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
                if len(rl) > 0:
                    print stdout.channel.recv(1024)

    def get_InteractionMatrices(self):
        HOname = self.CDMS.maps["HORecnCalibrat.RESULT_IM"].outfile
        TTname = self.CDMS.maps["TTRecnCalibrat.RESULT.IM"].outfile
        stdin, stdout, stderr = self.ssh.exec_command("cdmsSave -f "+self.remotepath+HOname+" HORecnCalibrat.RESULT_IM")
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
                if len(rl) > 0:
                    print stdout.channel.recv(1024)
        stdin, stdout, stderr = self.ssh.exec_command("cdmsSave -f "+self.remotepath+TTname+" TTRecnCalibrat.RESULT.IM")
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
                if len(rl) > 0:
                    print stdout.channel.recv(1024)
        self.ftp.get(self.remotepath+HOname, self.localpath+HOname)
        self.ftp.get(self.remotepath+TTname, self.localpath+TTname)
        return HOname, TTname
        

    def changePixelTapPoint(self, tp):
        try:
            if tp == "RAW":
                pass
            elif tp == "CALIB":
                pass
            elif tp == "BACKGROUND":
                pass
            else:
                print("Error!  Unrecognized tap point!")
                escape
            stdin, stdout, stderr = self.ssh.exec_command("cdmsSetProp Acq.CFG.DYNAMIC DET1.PIXEL_TAP -s \""+tp+"\"")
            while not stdout.channel.exit_status_ready():
                if stdout.channel.recv_ready():
                    rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
                    if len(rl) > 0:
                        print stdout.channel.recv(1024)
        except:
            print("Error!  Invalid tap point!")

    def measureBackground(self, nframes):
        stdin, stdout, stderr = self.ssh.exec_command("msgSend \"\" CommandGateway EXEC \"AcqOptimiser.measureBackground "+str(nframes)+"\"")
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
                if len(rl) > 0:
                    print stdout.channel.recv(1024)

    def updateAcq(self):
        stdin, stdout, stderr = self.ssh.exec_command("msgSend \"\" spaccsServer EXEC \"-command Acq.update ALL\"")
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
                if len(rl) > 0:
                    print stdout.channel.recv(1024)
    

class CDMS_Map( object ):
    def __init__(self, name, ax1, ax2, dtype, filltype, bscale):
        if dtype == "float32":
            self.dtype = numpy.float32
        elif dtype == "float16":
            self.dtype = numpy.float16
        elif dtype == "int32":
            self.dtype = numpy.int32
        elif dtype == "int16":
            self.dtype = numpy.int16
        else:
            print "Error!"
        if filltype == 0.0:
            self.data = numpy.zeros((ax1, ax2), dtype=self.dtype)
        elif filltype >= 1.0:
            self.data = numpy.ones((ax1, ax2), dtype=self.dtype)*filltype
        elif filltype == -1.0:
            self.data = numpy.arange(ax1, dtype=self.dtype)
        else:
            print "Error! I can't understand the fill type!"
        self.data_template = self.data.copy()
        self.bscale = bscale
        self.outfile = name+'.fits'

    def replace(self, newmap):
        self.data = self.dtype(newmap).copy()
        
    def revert(self):
        self.data = self.data_template.copy()

    def scale(self, factor):
        self.data *= factor

    def write(self, path=''):
        self.hdu = pyfits.PrimaryHDU(self.data)
        if self.bscale == 'minmax':
            self.hdu.scale(option='minmax')
        elif self.bscale == 'True':
            self.hdu.scale()
        warnings.resetwarnings()
        warnings.filterwarnings('ignore', category=UserWarning, append=True)
        self.hdu.writeto(path+self.outfile, clobber=True)
        warnings.resetwarnings()
        warnings.filterwarnings('always', category=UserWarning, append=True)


class CDMS( object ):
    def __init__(self):
        self.maps = {}
        self.populateMapDefs()

    def populateMapDefs(self):
        definitionFile = '/home/deen/Code/Python/BlurryApple/Tools/CDMS_Map_Definitions.dat'
        df = open(definitionFile, 'r')
        for line in df:
            l = line.split(',')
            name = l[0]
            ax1 = int(l[1])
            ax2 = int(l[2])
            dtype = l[3].strip()
            filltype = float(l[4])
            bscale = bool(l[5])
            self.maps[name] = CDMS_Map(name, ax1, ax2, dtype, filltype, bscale)


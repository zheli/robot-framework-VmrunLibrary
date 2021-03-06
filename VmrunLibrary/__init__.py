__version__ = '1.0'
import subprocess
import os, sys

class VmrunLibrary:
    """Vmrun Library is a test library for robot framework that controls vmware virtual machines by sending vmrun commands.
    """
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'
    ROBOT_LIBRARY_VERSION = __version__

    def __init__(self, vmbin, image, snapshot, guest_ip):
        self._status = 'OFFLINE'
        self._vmbin = '/usr/bin/vmrun'
        self._default_log_level = 'INFO'
        self._image = image
        self._snapshot = snapshot
        self._guest_ip = guest_ip

    def update_vm_status(self):
        self._status = self.get_status()

    def start_vm(self):
        self._info('starting snapshot [%s] for image: [%s]\nguest IP: [%s]' 
                % (self._snapshot, self._image, self._guest_ip))
        try:
            self._run('start')
        except:
            raise Exception('failed to start vm')
        else:
            return

    def suspend_vm(self, mode = 'soft'):
        self._info('suspending snapshot [%s] for image: [%s]\nguest IP: [%s]' 
                % (self._snapshot, self._image, self._guest_ip))
        try:
            self._run('suspend', mode)
        except:
            raise Exception('failed to suspend vm')
        else:
            return
        return

    def stop_vm(self, mode = 'soft'):
        self._info('stoping snapshot [%s] for image: [%s]\nguest IP: [%s]' 
                % (self._snapshot, self._image, self._guest_ip))
        try:
            self._run('stop', mode)
        except:
            raise Exception('failed to stop vm')
        else:
            return

    def create_snapshot(self, snapshot):
        if snapshot:
            self._info('creating snapshot [%s] for image: [%s]\nguest IP: [%s]'
                    % (snapshot, self._image, self._guest_ip))
            try:
                self._run('snapshot', snapshot)
            except:
                raise Exception('failed to create snapshot [%s]' % snapshot)
            else:
                return
        else:
            raise Exception('snapshot name required!')

    def delete_snapshot(self, snapshot):
        if snapshot:
            self._info('deleting snapshot [%s] from image: [%s]\nguest IP: [%s]'
                    % (snapshot, self._image, self._guest_ip))
            try:
                self._run('deleteSnapshot', snapshot)
            except:
                raise Exception('failed to remove snapshot [%s]' % snapshot)
            else:
                return
        else:
            raise Exception('snapshot name required!')

    def revert_to_snapshot(self, snapshot = None):
        if not snapshot:
            snapshot = self._snapshot
        self._info('reverting to snapshot [%s] for image: [%s]\nguest IP: [%s]'
                % (snapshot, self._image, self._guest_ip))
        try:
            self._run('revertToSnapshot', snapshot)
        except:
            raise Exception('failed to revert to snapshot [%s]' % snapshot)
        else:
            return

    def get_vm_status(self):
        try:
            response = subprocess.call('ping -c 1 %s' % self._guest_ip, 
                    shell=True, stdout=open('/dev/null', 'w'), 
                    stderr=subprocess.STDOUT)
        except:
            raise Exception('failed to ping')
        else:
            if 0 == response:
                return 'ONLINE'
            else:
                return 'OFFLINE'

    def _run(self, *cmd):
        cmds = list(cmd)
        cmds.insert(1, '"%s"' % self._image)
        params = ' '.join(cmds)
        self._debug('execute vmrun [%s]' % params)
        cmd = ["sh", "-c", "%s %s" % (self._vmbin, params)]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)

        return p.stdout.readlines()

    def _debug(self, msg):
        self._log(msg, 'DEBUG')

    def _info(self, msg):
        self._log(msg, 'INFO')

    def _log(self, msg, level = None):
        msg = msg.strip()
        if not level:
            level = self._default_log_level
        if msg:
            print('*%s* %s' % (level.upper(), msg))

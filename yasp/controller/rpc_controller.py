####################################################################################################
#    Copyright (C) 2016-2017 by Ingo Keller                                                             #
#    <brutusthetschiepel@gmail.com>                                                                #
#                                                                                                  #
#    This file is part of YASP (Yet Another Speech Package).                                       #
#                                                                                                  #
#    YASP is free software: you can redistribute it and/or modify it under the terms of the        #
#    GNU Affero General Public License as published by the Free Software Foundation, either        #
#    version 3 of the License, or (at your option) any later version.                              #
#                                                                                                  #
#    YASP is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;             #
#    without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.     #
#    See the GNU Affero General Public License for more details.                                   #
#                                                                                                  #
#    You should have received a copy of the GNU Affero General Public License                      #
#    along with YASP.  If not, see <http://www.gnu.org/licenses/>.                                 #
####################################################################################################
import yarp


class RpcController(object):


    def _getClient(self, output):
        _rpc_client = yarp.RpcClient()
        _port_name = "/" + self.__class__.__name__ + "/" + str(id(self)) + "/cmd"
        _rpc_client.open(_port_name)
        _rpc_client.addOutput(output)
        return _rpc_client, _port_name


    def _execute(self, cmd):
        """Execute an RPC command, returning obtained answer bottle."""
        ans = yarp.Bottle()     
        self._rpc_client.write(cmd, ans)
        return ans


    def _is_success(self, ans):
        """Check if RPC call answer Bottle indicates successfull execution."""
        return ans.size() == 1 and ans.get(0).asVocab() == 27503 # Vocab for '[ok]'

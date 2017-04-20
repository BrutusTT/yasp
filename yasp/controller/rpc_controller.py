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

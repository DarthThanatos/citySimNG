package rankingnode;

import org.json.JSONObject;

import model.DependenciesRepresenter;
import controlnode.DispatchCenter;
import controlnode.SocketNode;

public class RankingNode extends SocketNode {

	public RankingNode(DependenciesRepresenter dr, DispatchCenter dispatchCenter, String nodeName){
		super(dr, dispatchCenter, nodeName);
	}

	@Override
	public String parseCommand(String command, JSONObject args) {
		return "{}";
	}


	@Override
	public void atStart() {
		// TODO Auto-generated method stub
		
	}


	@Override
	public void atExit() {
		// TODO Auto-generated method stub
		
	}


	@Override
	public void atUnload() {
		// TODO Auto-generated method stub
		
	}

}

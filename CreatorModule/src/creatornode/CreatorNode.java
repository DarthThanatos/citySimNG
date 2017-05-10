//* Init class responsible for creating new games with given parameters. Will be implemented in future. */ 

package creatornode;
import org.json.JSONObject;

import model.DependenciesRepresenter;
import controlnode.DispatchCenter;
import controlnode.Node;
import controlnode.SocketNode;

public class CreatorNode extends SocketNode{
	
	public CreatorNode(DependenciesRepresenter dr, DispatchCenter dispatchCenter, String nodeName) {
		super(dr, dispatchCenter, nodeName);
		System.out.println("Created Creator Node");
	}

	@Override
	public String parseCommand(String command, JSONObject args) {
		if(command.equals("Parse")){
			System.out.println("Creator node received following dependencies package:\n" + args.getJSONObject("Dependencies"));
		}
		return "Creator@Msg received successfully";
	}

	@Override
	public void atStart() {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void atExit() {
		// TODO Auto-generated method stub
		
	}

}

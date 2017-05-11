//* Init class responsible for creating new games with given parameters. Will be implemented in future. */ 

package creatornode;
import org.json.JSONObject;

import model.DependenciesRepresenter;
import controlnode.DispatchCenter;
import controlnode.Node;
import controlnode.SocketNode;

public class CreatorNode extends SocketNode{
	
	public CreatorNode(DispatchCenter dispatchCenter, String nodeName) {
		super(dispatchCenter, nodeName);
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

	@Override
	public void atUnload() {
		// TODO Auto-generated method stub
		
	}

}

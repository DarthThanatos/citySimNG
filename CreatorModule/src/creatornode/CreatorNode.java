//* Init class responsible for creating new games with given parameters. Will be implemented in future. */ 

package creatornode;
import model.DependenciesRepresenter;
import controlnode.Node;
import controlnode.SocketNode;

public class CreatorNode extends SocketNode{
	
	public CreatorNode(DependenciesRepresenter dr) {
		super(dr);
		System.out.println("Created Creator Node");
		nodeName = "CreatorNode";
	}

	@Override
	public String parseCommand(String command, String[] streamArgs) {
		if(command.equals("Parse")){
			String jsonDependencies = streamArgs[0].replace(",", ",\n");
			System.out.println("Creator node received following dependencies package:\n" + jsonDependencies);
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

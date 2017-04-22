package tutorialnode;

import model.DependenciesRepresenter;
import controlnode.SocketNode;

public class TutorialNode extends SocketNode{

	public TutorialNode(DependenciesRepresenter dr) {
		super(dr);
		System.out.println("Created Tutorial Node");
		nodeName = "TutorialNode";
	}


	/*
	 * (non-Javadoc)
	 * @see controlnode.Node#parseCommand(java.lang.String, java.lang.String[])
	 * returns - output stream understandable to the current entity in the view layer (here TutorialView)
	 */
	@Override
	public String parseCommand(String command, String[] streamArgs) {
		return "pass";
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

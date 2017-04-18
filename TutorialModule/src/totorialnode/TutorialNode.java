package totorialnode;

import model.DependenciesRepresenter;
import controlnode.SocketNode;

public class TutorialNode extends SocketNode{

	public TutorialNode(SocketNode parent, DependenciesRepresenter dr) {
		super(parent, dr);
	}

	@Override
	public void createChildren() {
		/*
		 * this node has no children; skipping...
		 */
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

}

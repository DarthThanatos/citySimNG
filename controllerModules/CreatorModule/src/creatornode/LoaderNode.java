package creatornode;

import java.util.ArrayList;



import java.util.HashMap;

import model.DependenciesRepresenter;
import monter.LoaderMonter;

import org.json.JSONObject;

import controlnode.DispatchCenter;
import controlnode.Node;
import controlnode.SocketNode;

public class LoaderNode extends SocketNode{

	public LoaderNode(DispatchCenter dispatchCenter, String nodeName) {
		super(dispatchCenter, nodeName);
		// TODO Auto-generated constructor stub
	}

	@Override
	public String parseCommand(String command, JSONObject args) {
		JSONObject envelope = new JSONObject();
		envelope.put("To", "Loader");
		if(command.equals("Select")){
			System.out.println(nodeName + ": got string selection: " + args.getString("SetChosen"));
			String operationId = args.getString("UUID");
			JSONObject ackArgs = new JSONObject();
			ackArgs.put("UUID",operationId);
			envelope.put("Operation", "SelectConfirm");
			envelope.put("Args", ackArgs);
			
			//dynamically mount new set of rules
			System.out.println("Loader: dispatch: " + dispatchCenter);
			LoaderMonter monter = new LoaderMonter("resources\\injectFiles\\loaderInject.txt", new String[]{}, dispatchCenter, new DependenciesRepresenter());
			Node menu = monter.mount(new ArrayList<String>());
			menu.setParent(nodeName, this);
			neighbors = new HashMap<>();
			neighbors.put(menu.getNodeName(),menu);
			neighbors.put(parent.getNodeName(),parent);
		}
		return envelope.toString();
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

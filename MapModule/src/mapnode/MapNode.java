package mapnode;

import model.DependenciesRepresenter;

import java.io.BufferedReader;
import java.io.InputStreamReader;

import controlnode.Node;
import controlnode.SocketNode;
import controlnode.SocketStreamSender;

public class MapNode extends SocketNode{

	public MapNode(DependenciesRepresenter dr) {
		super(dr);
		System.out.println("Created Map Node");
		nodeName = "MapNode";
	}

	@Override
	public Node nodeLoop(){
		try{
		sender = new SocketStreamSender(nodeName);
		sender.start();
		}catch(Exception e){}
		Runnable resourcesThread = new Runnable() {
			public void run() {
				new Resources(sender).updateResources();
			}
		};
		resourcesThread.run();
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		try{
		br.readLine();
		}catch(Exception e){}
		return null;
	}
	
	@Override
	public String parseCommand(String command, String[] streamArgs) {
		// TODO Auto-generated method stub
		return null;
	}


}

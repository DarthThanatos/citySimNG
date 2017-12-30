package monter;

import java.io.*;
import java.lang.reflect.Constructor;
import java.net.URL;
import java.net.URLClassLoader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

import constants.Consts;
import controlnode.DispatchCenter;
import controlnode.Node;

public class BaseMonter implements SystemMonter{

	private static final Logger logger = Logger.getLogger( BaseMonter.class.getName() );
	private List<String> textDescriptions;
	HashMap<String, Node> nodes;
	protected DispatchCenter dispatchCenter;
	String currentLocation = System.getProperty("user.dir");;

	BaseMonter(String filePath, DispatchCenter dispatchCenter){
		logger.setLevel(Consts.DEBUG_LEVEL);
		BufferedReader br = null;
		this.dispatchCenter = dispatchCenter == null ? new DispatchCenter() : dispatchCenter;
		try {
			br = new BufferedReader(new FileReader(new File(filePath)));
			textDescriptions = new LinkedList<>();
			String line;
			while((line = br.readLine())!= null){
				textDescriptions.add(line);
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
		finally{
			try {
				assert br != null;
				br.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
		nodes = new HashMap<>();
		
	}
	
	public BaseMonter(String filePath){
		this(filePath,  (DispatchCenter)null);
	}

	public BaseMonter(String filePath, String currentLocation){
		this(filePath,  (DispatchCenter)null);
		this.currentLocation = currentLocation;
	}

	protected void readNodes(String[] nodeDesc, ArrayList<String> modulesNames){
		String projectName = nodeDesc[0];
		String nodeClassName = nodeDesc[1];
		String nodeHashKey = nodeDesc[2];
		modulesNames.add(nodeHashKey);
		
		URLClassLoader urlLoader = null;
		logger.log(Level.INFO,"Read and create node " + nodeClassName + " with a hash key " + nodeHashKey );
     	try {
     		/*Using java reflection to dynamically load Node instances from other modules(which are set up as separate projects)*/
//			String currentLocation = System.getProperty("user.dir");
			String urlStr = "file:///" + currentLocation + "/" +  projectName + "/bin/"; //+ nodeClassName + ".class";//"MenuModule\\bin\\menunode\\MenuNode.class";
			logger.info("using url: " + urlStr);
			URL[] urls = {new URL (urlStr)};
			urlLoader = new URLClassLoader(urls);
			Class<?> nodeClass = urlLoader.loadClass(nodeClassName);
			Constructor<?> constructor = nodeClass.getConstructor(DispatchCenter.class, String.class);
			Node node = (Node)constructor.newInstance(dispatchCenter, nodeHashKey);
			nodes.put(nodeHashKey, node);
		} catch (Exception e) {
			logger.log(Level.SEVERE,"Not found: " + nodeClassName );
		} 
     	finally{
     		try {
				assert urlLoader != null;
				urlLoader.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
     	}	
	}
	
	/*
	 * method for creating relationships between Node instances;
	 * expects a two-element String array, where the first element 
	 * contains "from" key referencing the parent node, 
	 * and the second is the node to which the parent node passes control
	 * e.g. there exists an edge MenuNode -> CreatorNode: edgeDesc[0] = MenuNode, edgeDesc[1] = CreatorNode
	 */
	private void readEdges(String[] edgeDesc){
		Node fromNode =  nodes.get(edgeDesc[0]);
		Node toNode = nodes.get(edgeDesc[1]);
		fromNode.addNeighbour(edgeDesc[1], toNode);
		toNode.setParent(edgeDesc[0], fromNode);
	}
		
	/*
	 * (non-Javadoc)
	 * @see monter.SystemMonter#mount()
	 * 
	 */
	@Override
	public Node mount(ArrayList<String> modulesNamesList) {
		
		String mode = ""; /*text establishing the mode of parsing*/
		String mainNodeName = ""; 
		/* 
		 * ^ hashKey of the main node received from the configuration file; 
		 * is used to return proper Node instance, from which control starts to flow 
		 */
		
		for(String description : textDescriptions){
			if(description.startsWith("#")) {
				/*dismiss comments*/
				continue; 
			}

			if (description.replaceAll("\\s+", "").equals("")) {
				/*if there are no alpha numerical characters, we can skip this "description*/
				continue; /*dismiss empty lines*/
			}
			
			String[] descriptionParts = description.split(" ");

			/*Phase one: establish if mode changed*/
			if(descriptionParts[0].equals("Mode")){
				mode = descriptionParts[1];
				continue;
			}
			
			/* 
			 * Act accordingly to the mode selected earlier; 
			 * by now we know that a line of text is not a comment;
			 * thus it is expected to be a valid part of the description, structured in  
			 * a legitimate way, so current mode of mounting can understand it 
			*/
			switch (mode) {
				case "Nodes":
					readNodes(descriptionParts, modulesNamesList);
					break;
				case "Edges":
					readEdges(descriptionParts);
					break;
				case "StartNode":
				/*
				 * expecting, that the line of text stored under the variable
				 * "description", is an actual hashKey of the node, mentioned at least once
				 * during the operation of previous modes
				 */

					mainNodeName = description;
					break;
				default:
					logger.log(Level.SEVERE,"Invalid mode selected, kernel panic" );
					return null;
			}
		}
		dispatchCenter.createDB(modulesNamesList);
		return nodes.get(mainNodeName);

	}

}

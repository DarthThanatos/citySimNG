package monter;

import java.io.IOException;
import java.lang.reflect.Constructor;
import java.net.URL;
import java.net.URLClassLoader;
import java.util.ArrayList;

import model.DependenciesRepresenter;
import controlnode.DispatchCenter;
import controlnode.Node;

public class LoaderMonter extends BaseMonter{

	private DependenciesRepresenter dr;
	
	public LoaderMonter(String filePath, String[] args, DispatchCenter dispatchCenter, DependenciesRepresenter dr) {
		super(filePath, args, dispatchCenter);
		this.dr = dr; 
	}
	
	@Override 
	protected void readNodes(String[] nodeDesc, ArrayList<String> modulesNames){
		String projectName = nodeDesc[0];
		String nodeClassName = nodeDesc[1];
		String nodeHashKey = nodeDesc[2];
		modulesNames.add(nodeHashKey);
		
		URLClassLoader urlLoader = null; 
		System.out.println("Read and create node " + nodeClassName + " with a hash key " + nodeHashKey);
     	try {
     		/*Using java reflection to dynamically load Node instances from other modules(which are set up as separate projects)*/
			String currentLocation = System.getProperty("user.dir");
			System.out.println("Current location: " + currentLocation);
			String urlStr = "file:///" + currentLocation + "/" +  projectName + "/bin/"; //+ nodeClassName + ".class";//"MenuModule\\bin\\menunode\\MenuNode.class";
			System.out.println("Url: " + urlStr);
			URL[] urls = {new URL (urlStr)};
			urlLoader = new URLClassLoader(urls);
			Class<?> nodeClass = urlLoader.loadClass(nodeClassName);
			Constructor<?> constructor = nodeClass.getConstructor(DependenciesRepresenter.class, DispatchCenter.class, String.class);
			Node node = (Node)constructor.newInstance(dr, dispatchCenter, nodeHashKey);
			nodes.put(nodeHashKey, node);
		} catch (Exception e) {
			System.err.println("Not found: " + nodeClassName);
			e.printStackTrace();
		} 
     	finally{
     		try {
				urlLoader.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
     	}		
	}

}

package monter;

import java.io.IOException;
import java.lang.reflect.Constructor;
import java.net.URL;
import java.net.URLClassLoader;
import java.util.ArrayList;
import java.util.logging.Logger;

import model.DependenciesRepresenter;
import controlnode.DispatchCenter;
import controlnode.Node;

public class LoaderMonter extends BaseMonter{

	private DependenciesRepresenter dr;
	private static final Logger logger = Logger.getLogger( LoaderMonter.class.getName() );
	
	public LoaderMonter(String filePath, DispatchCenter dispatchCenter, DependenciesRepresenter dr) {
		super(filePath, dispatchCenter);
		this.dr = dr; 
	}
	public LoaderMonter(String filePath, DispatchCenter dispatchCenter, DependenciesRepresenter dr, String currentLocation){
		this(filePath, dispatchCenter, dr);
		this.currentLocation = currentLocation;
	}

	@Override 
	protected void readNodes(String[] nodeDesc, ArrayList<String> modulesNames){
		String projectName = nodeDesc[0];
		String nodeClassName = nodeDesc[1];
		String nodeHashKey = nodeDesc[2];
		modulesNames.add(nodeHashKey);
		
		URLClassLoader urlLoader = null;
     	try {
     		/*Using java reflection to dynamically load Node instances from other modules(which are set up as separate projects)*/
//			String currentLocation = System.getProperty("user.dir");
			String urlStr = "file:///" + currentLocation + "/" +  projectName + "/bin/"; //+ nodeClassName + ".class";//"MenuModule\\bin\\menunode\\MenuNode.class";
			logger.info("using url: " + urlStr);
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
				assert urlLoader != null;
				urlLoader.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
     	}		
	}

}

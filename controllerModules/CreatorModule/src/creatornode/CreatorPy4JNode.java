package creatornode;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.Set;

import org.json.JSONArray;
import org.json.JSONObject;

import py4jmediator.CreatorData;
import py4jmediator.Presenter;
import model.DependenciesRepresenter;
import constants.Consts;
import constants.CreatorConfig;
import controlnode.DispatchCenter;
import controlnode.Py4JNode;
import corectness.checker.CheckException;
import dependencies.graph.monter.BuildingsMonter;
import dependencies.graph.monter.DwellersMonter;
import dependencies.graph.monter.ResourcesMonter;
import py4jmediator.*;

public class CreatorPy4JNode extends Py4JNode implements CreatorPresenter.OnCreatorPresenterCalled {

	public CreatorPy4JNode(DispatchCenter dispatchCenter, String nodeName) {
		super(null, dispatchCenter, nodeName);
		createDefaultDependencies();
	}

	@Override
	public void atUnload() {

		
	}

	@Override
	protected void atStart() {
		CreatorPresenter creatorPresenter = Presenter.getInstance().getCreatorPresenter(); 
		creatorPresenter.setOnCreatorPresenterCalled(this);
		creatorPresenter.displayCreator();
		
	}

	@Override
	protected void onLoop() {
		
	}

	@Override
	protected void atExit() {
		Presenter.getInstance().getCreatorPresenter().setOnCreatorPresenterCalled(null);	
	}
	
	private String loadDefaultDependenciesString() throws IOException{
		BufferedReader br = new BufferedReader(new FileReader(new File("resources\\dependencies\\new_stronghold.dep")));
		String dependenciesString = "", line;
		while( (line = br.readLine()) != null ){
			dependenciesString += line + "\n";
		}
		br.close();
		return dependenciesString;
	}
	
	private static JSONArray retrieveArrayFromObj(JSONObject obj){
		JSONArray resArray = new JSONArray();
		Set<String> names = obj.keySet(); 
		for (String name : names){
			resArray.put(obj.getJSONObject(name));
		}
		return resArray;
	}
	
	private DependenciesRepresenter initDefaultDependenciesRepresenter() throws IOException{
		DependenciesRepresenter dr = new DependenciesRepresenter();
		
		String dependenciesString = loadDefaultDependenciesString();
		JSONObject dependencies = new JSONObject(dependenciesString);
		
		JSONArray resources = retrieveArrayFromObj(dependencies.getJSONObject("Resources"));		
		JSONArray buildings = retrieveArrayFromObj(dependencies.getJSONObject("Buildings"));
		JSONArray dwellers = retrieveArrayFromObj(dependencies.getJSONObject("Dwellers"));
		
		ResourcesMonter rm = new ResourcesMonter(resources, dr);
		BuildingsMonter bm = new BuildingsMonter(buildings, dr);
		DwellersMonter dm = new DwellersMonter(dwellers, dr);
		
		try {
			rm.mountDependenciesGraph();
		    dm.mountDependendenciesGraph();
		    bm.mountDependenciesGraph();
		}
		catch(Exception e){
			e.printStackTrace();
		}
		
		dr.setTextureAt(0, CreatorConfig.TEXTURE_ONE_DEFAULT_NAME);
		dr.setTextureAt(1, CreatorConfig.TEXTURE_TWO_DEFAULT_NAME);
		
		return dr;
	}
	
	private HashMap<String, DependenciesRepresenter> fetchRepresentersMap(){
		HashMap<String, DependenciesRepresenter> representers = null;
		try{
			 representers = 
				 (HashMap<String, DependenciesRepresenter>) dispatchCenter
				 	.getDispatchData(Consts.LOADER_MODULE, Consts.DEPENDENCIES_REPRESENTERS);
		}
		catch(Exception e){
			representers = new HashMap<>();	
			dispatchCenter
				.putDispatchData(Consts.LOADER_MODULE, Consts.DEPENDENCIES_REPRESENTERS, representers);
		}
		return representers;
	}
	
	private void createDefaultDependencies(){
		try {
			DependenciesRepresenter dr = initDefaultDependenciesRepresenter();
			HashMap<String, DependenciesRepresenter> representers = fetchRepresentersMap();
			representers.put(CreatorConfig.DEPENDENCIES_DEFAULT_SET_NAME, dr);
		} catch (Exception e) {
			e.printStackTrace();
		} 
	}
	
	private DependenciesRepresenter initDependenciesRepresenter(CreatorData creatorData) throws CheckException{
		DependenciesRepresenter dr = new DependenciesRepresenter();
		ResourcesMonter rm = new ResourcesMonter(creatorData.getResources(), dr);
		BuildingsMonter bm = new BuildingsMonter(creatorData.getBuildings(), dr);
		DwellersMonter dm = new DwellersMonter(creatorData.getDwellers(), dr);	
		rm.mountDependenciesGraph();
	    dm.mountDependendenciesGraph();
	    bm.mountDependenciesGraph();
		String textureOne = creatorData.getTextureOne();
		String textureTwo =  creatorData.getTextureTwo();
		dr.setTextureAt(0, textureOne != null ? textureOne : CreatorConfig.TEXTURE_ONE_DEFAULT_NAME);
		dr.setTextureAt(1, textureTwo != null ? textureTwo : CreatorConfig.TEXTURE_TWO_DEFAULT_NAME);
		return dr;
		
	}

	@Override
	public void onCreateDependencies(CreatorData creatorData) {
		DependenciesRepresenter dr;
		CreatorPresenter creatorPresenter = Presenter.getInstance().getCreatorPresenter();
		try {
			dr = initDependenciesRepresenter(creatorData);
			HashMap<String, DependenciesRepresenter> representers = fetchRepresentersMap();
			representers.put(creatorData.getDependenciesSetName(), dr);
			creatorPresenter.displayDependenciesGraph( dr.getGraphsHolder().displayAllGraphs());
			creatorPresenter.displayMsg("Dependencies created successfully, please go to the Loader menu now to check what was created");
		} catch (CheckException e) {
			creatorPresenter.displayMsg(e.getMessage());
		}
	}

	@Override
	public void onReturnToMenu() {
		moveTo("MainMenuNode");
	}

}

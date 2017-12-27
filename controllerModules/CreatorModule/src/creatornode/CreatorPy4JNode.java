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
		createDefaultDependencies( "resources\\sysFiles\\defaultDependencies\\");
	}

	public CreatorPy4JNode(DispatchCenter dispatchCenter, String nodeName, String defaultFilesPrefix){
		super(null, dispatchCenter, nodeName);
		createDefaultDependencies(defaultFilesPrefix);
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
	protected void atExit() {
		Presenter.getInstance().getCreatorPresenter().setOnCreatorPresenterCalled(null);	
	}
	
	private String loadDefaultDependenciesString(String fileName) throws IOException{
		BufferedReader br = new BufferedReader(new FileReader(new File(fileName)));
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
	
	private DependenciesRepresenter initDefaultDependenciesRepresenter(String fileName) throws IOException{
		DependenciesRepresenter dr = new DependenciesRepresenter();
		
		String dependenciesString = loadDefaultDependenciesString(fileName);
		JSONObject dependencies = new JSONObject(dependenciesString);
		
		JSONArray resources = retrieveArrayFromObj(dependencies.getJSONObject("Resources"));		
		JSONArray buildings = retrieveArrayFromObj(dependencies.getJSONObject("Buildings"));
		JSONArray dwellers = retrieveArrayFromObj(dependencies.getJSONObject("Dwellers"));

		dr.setPanelTexture(dependencies.getString(Consts.PANEL_TEXTURE));
		dr.setTextureAt(0, dependencies.getString(Consts.TEXTURE_ONE));
		dr.setTextureAt(1, dependencies.getString(Consts.TEXTURE_TWO));
		dr.setMp3(dependencies.getString(Consts.MP3));

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

	private void createDefaultDependencies(String defaultDepsPathPrefix){
		try {
			HashMap<String, DependenciesRepresenter> representers = fetchRepresentersMap();
			DependenciesRepresenter dr = initDefaultDependenciesRepresenter(defaultDepsPathPrefix + "new_stronghold.dep");
			representers.put(CreatorConfig.DEPENDENCIES_DEFAULT_SET_NAME_ONE, dr);
			dr = initDefaultDependenciesRepresenter(defaultDepsPathPrefix + "moon.dep");
			representers.put(CreatorConfig.DEPENDENCIES_DEFAULT_SET_NAME_TWO, dr);
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
		dr.setTextureAt(0, textureOne);
		dr.setTextureAt(1, textureTwo);
		dr.setPanelTexture(creatorData.getPanelTexture());
		dr.setMp3(creatorData.getMp3());
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
			creatorPresenter.displayMsg("Dependencies created successfully, please go to the Loader menu now to mapLevels what was created");
		} catch (CheckException e) {
			creatorPresenter.displayMsg(e.getMessage());
		}
	}

	@Override
	public void onReturnToMenu() {
		moveTo("MainMenuNode");
	}

}

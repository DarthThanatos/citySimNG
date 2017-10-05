package creatornode;

import java.util.ArrayList;
import java.util.HashMap;

import model.DependenciesRepresenter;
import monter.LoaderMonter;
import controlnode.DispatchCenter;
import controlnode.Node;
import controlnode.Py4JNode;
import py4jmediator.*;

public class LoaderPy4JNode extends Py4JNode implements LoaderPresenter.OnLoaderPresenterCalled{

	private Node currentGameMenuNode = null;

	public LoaderPy4JNode(DependenciesRepresenter dr,
			DispatchCenter dispatchCenter, String nodeName) {
		super(dr, dispatchCenter, nodeName);
	}

	public LoaderPy4JNode(DispatchCenter dispatchCenter, String nodeName) {
		this(null,dispatchCenter, nodeName);
	}
	
	@Override
	public void atUnload() {
		
	}


	@Override
	protected void onLoop() {
		
	}
	
	@Override
	protected void atStart() {
		LoaderPresenter loaderPresenter = Presenter.getInstance().getLoaderPresenter();
		loaderPresenter.setOnLoaderPresenterCalled(this);
		loaderPresenter.displayLoader();		
		initPossipleDependenciesSets();
		if(currentGameMenuNode != null) currentGameMenuNode.atUnload();
	}


	@Override
	protected void atExit() {
		Presenter.getInstance().getLoaderPresenter().setOnLoaderPresenterCalled(null);
	}

	@Override
	public void onGoToMainMenu() {
		moveTo("MainMenuNode");
	}

	@Override
	public void onGoToGameMenu() {
		moveTo("GameMenuNode");
	}

	private DependenciesRepresenter fetchDependenciesRepresenter(String chosenSet){
		HashMap<String, DependenciesRepresenter> representers = fetchRepresentersMap();
		return representers.get(chosenSet);
	}
	
	@Override
	public void onShowGraph(String chosenSet) {
		Presenter.getInstance().getLoaderPresenter().displayGraph(fetchDependenciesRepresenter(chosenSet).getGraphsHolder().displayAllGraphs());
	}
	
	private Node mountGraph(DependenciesRepresenter chosenDR){
		LoaderMonter monter = new LoaderMonter("resources\\injectFiles\\loaderInject.txt", new String[]{}, dispatchCenter, chosenDR);
		return monter.mount(new ArrayList<String>());	
	}
	
	private void connectMountedGraph(Node menu){
		menu.setParent(nodeName, this);
		neighbors = new HashMap<>();
		neighbors.put(menu.getNodeName(),menu);
		neighbors.put(parent.getNodeName(),parent);
	}
	
	private void mountDependenciesRules(DependenciesRepresenter chosenDR){
		//dynamically mount new set of rules
		currentGameMenuNode = mountGraph(chosenDR);
		connectMountedGraph(currentGameMenuNode);
	}
	
	@Override
	public void onSelectDependenciesGraph(String chosenSet){
		DependenciesRepresenter dr = fetchDependenciesRepresenter(chosenSet);
		mountDependenciesRules(dr);
	}
	
	private void initPossipleDependenciesSets(){
		HashMap<String, DependenciesRepresenter> representers = fetchRepresentersMap();
		Presenter.getInstance().getLoaderPresenter().displayPossibleDependenciesSets(representers.keySet());
	}

	private HashMap<String, DependenciesRepresenter> fetchRepresentersMap(){
		HashMap<String, DependenciesRepresenter> representers = null;
		try{
			representers = (HashMap<String, DependenciesRepresenter>) dispatchCenter.getDispatchData("LoaderModule", "DependenciesRepresenters");
		}
		catch(Exception e){
			representers = new HashMap<String, DependenciesRepresenter>();
			dispatchCenter.putDispatchData("LoaderModule", "DependenciesRepresenters", representers);
		}
		return representers;
	}
	
}

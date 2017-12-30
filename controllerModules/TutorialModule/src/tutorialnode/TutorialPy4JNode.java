package tutorialnode;

import java.util.*;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

import entities.Building;
import entities.Entity;
import hintsender.HintSender;
import org.json.JSONObject;
import org.json.JSONArray;

import model.DependenciesRepresenter;
import graph.GraphsHolder;
import graph.BuildingNode;
import graph.DwellerNode;
import graph.ResourceNode;
import graph.GraphNode;

import controlnode.DispatchCenter;

import py4jmediator.Presenter;
import controlnode.Py4JNode;
import py4jmediator.*;

public class TutorialPy4JNode extends Py4JNode implements TutorialPresenter.OnTutorialPresenterCalled{

	private JSONObject readPage;
	private BufferedReader tutorialReader;
	private HintSender hintSender;
	private String[] tutorialIndex;
	private int tutorialIndexEntries;
	private List<String> buildingsIndex;
	private List<String> resourcesIndex;
	private List<String> dwellersIndex;
	private GraphsHolder graphsHolder;

	public TutorialPy4JNode(DependenciesRepresenter dr, DispatchCenter dispatchCenter, String nodeName) {
		super(dr, dispatchCenter, nodeName);
		readPage = new JSONObject("{}");
		hintSender = new HintSender(this, dispatchCenter.getEventBus());

		buildingsIndex = new ArrayList<String>();
		resourcesIndex = new ArrayList<String>();
		dwellersIndex = new ArrayList<String>();
	}


	/*
	 * (non-Javadoc)
	 * @see controlnode.Node#parseCommand(java.lang.String, java.lang.String[])
	 * returns - output stream understandable to the current entity in the view layer (here TutorialView)
	 */
	private enum ENTITY_ENUM {
		BUILDING_HINT_CODE, RESOURCE_HINT_CODE, DWELLER__HINT_CODE
	};

	private <E extends Entity> String getOneDescSentence(E entity){
		String[] descSentences = entity.getDescription().split("\\.");
		return descSentences[Math.abs(new Random().nextInt()) % descSentences.length] + ".";
	}

	private<E extends Entity> String getHintFromEntityDescription(E entity){
//		return getOneDescSentence(entity);
		return entity.getName() + ": " + entity.getDescription();
	}

	public String getHints(){
		//TODO, actual hints and synchronized block
		ENTITY_ENUM entityToHintAbout =  ENTITY_ENUM.values()[Math.abs(new Random().nextInt()) % 3];
		String result = "";
		switch(entityToHintAbout){
			case BUILDING_HINT_CODE:
				result += getHintFromEntityDescription(dr.getGraphsHolder().getRandomBuilding());
				break;
			case RESOURCE_HINT_CODE:
				result += getHintFromEntityDescription(dr.getGraphsHolder().getRandomResource());
				break;
			case DWELLER__HINT_CODE:
				result += getHintFromEntityDescription(dr.getGraphsHolder().getRandomDweller());
				break;
		}
		return result;
	}


	public void readPage(int pageID) throws IOException{
		String line;
		String page = "";
			tutorialReader = new BufferedReader(new FileReader ("resources\\Tutorial\\page"+pageID+".json"));
			while ((line = tutorialReader.readLine()) != null) {
				System.out.println("line = " + line);
				page = page.concat(line); 
			}
			tutorialReader.close();

			page = page.replaceAll("[\\p{Cc}\\p{Cf}\\p{Co}\\p{Cn}]", "?");
			System.out.println("Pure string: " + page);
			readPage = new JSONObject(page);
			System.out.println("Read page:" + readPage.toString());
	}


	@Override
	public void atStart() {
		graphsHolder = dr.getGraphsHolder();
		TutorialPresenter tutorialPresenter = Presenter.getInstance().getTutorialPresenter();
		tutorialPresenter.setOnTutorialPresenterCalled(this);
		tutorialPresenter.displayTutorial();

		JSONObject graphs = graphsHolder.displayAllGraphs();
		JSONObject envelope = new JSONObject();
			envelope.put("Args", graphs);
		Presenter.getInstance().getTutorialPresenter().displayDependenciesGraph(envelope);

		//fetch tutorialIndex
		String line;
		String page = "";
			try {
				tutorialReader = new BufferedReader(new FileReader ("resources\\Tutorial\\tutorialIndex.json"));
				while ((line = tutorialReader.readLine()) != null) {
					System.out.println("line = " + line);
					page = page.concat(line); 
				}
				tutorialReader.close();
			}catch (IOException e){
				e.printStackTrace();
			}

			page = page.replaceAll("[\\p{Cc}\\p{Cf}\\p{Co}\\p{Cn}]", "?");
			System.out.println("Pure string: " + page);
			readPage = new JSONObject(page);
			System.out.println("Read page:" + readPage.toString());
			tutorialIndexEntries = readPage.length()-1;
			tutorialIndex = new String[readPage.length()+1];
			int nr;
			String keyName;
			for (Iterator<String> key = readPage.keys(); key.hasNext();){
				keyName = key.next();
				nr = readPage.getInt(keyName);
				tutorialIndex[nr] = keyName;
			}

		//fetch buildings, dwellers, etc/
		System.out.println("PROCESS BUILDINGS");
		for (BuildingNode n : graphsHolder.getBuildingsGraphs()) {
			buildingsIndex.add(n.getName());
			getAllNodes(buildingsIndex, n, 'b');
		}
		System.out.println("PROCESS RESOURCES");
		for (ResourceNode n : graphsHolder.getResourcesGraphs()) {
			resourcesIndex.add(n.getName());
			getAllNodes(resourcesIndex, n, 'r');
		}
		System.out.println("PROCESS DWELLERS");
		for (DwellerNode n : graphsHolder.getDwellersGraphs()) {
			dwellersIndex.add(n.getName());
			getAllNodes(dwellersIndex, n , 'd');
		}

		//handle tutorialIndex to python view
		Presenter.getInstance().getTutorialPresenter().fetchTutorialIndex(tutorialIndex);
		Presenter.getInstance().getTutorialPresenter().fetchNodes(buildingsIndex, resourcesIndex, dwellersIndex);
	}

	private void getAllNodes(List<String> nodesIndex, GraphNode node, char type){
		Map<String, GraphNode> children = node.getChildren();
		for (String nextName : children.keySet()) {
				System.out.println("got " + nextName);
				nodesIndex.add(nextName);
				if (type == 'b'){
					BuildingNode successor = graphsHolder.getBuildingNode(nextName);
					getAllNodes(nodesIndex, successor, 'b');
				}
				else if (type == 'r'){
					ResourceNode successor = graphsHolder.getResourceNode(nextName);
					getAllNodes(nodesIndex, successor, 'r');
				}
				else if (type == 'd'){
					DwellerNode successor = graphsHolder.getDwellerNode(nextName);
					getAllNodes(nodesIndex, successor, 'd');
				}
				else
					System.out.println("Something went wrong (java, getAllNodes");
		}
	}


	@Override
	public void atExit() {
		Presenter.getInstance().getTutorialPresenter().setOnTutorialPresenterCalled(null);	
	}


	@Override
	public void atUnload() { 
		hintSender.atUnload();
	}

	@Override
	public void onReturnToMenu(){ 
		moveTo("GameMenuNode");
	}

	@Override
	public void onFetchPage(int pageNr){
		int tabID = (int)(pageNr/10);
		System.out.println("JAVAAAAA tabID: "+ tabID);
        if (tabID == 1)
        	onFetchTutorialPage(pageNr);
		else if (tabID == 2)
			onFetchBuildingPage(pageNr);
		else if (tabID == 3) 
			onFetchResourcePage(pageNr);
		else if (tabID == 4)
			onFetchDwellerPage(pageNr);
		else
			System.out.println("Something went wrong! (java, onFetchPage()");
	}

	public void onFetchTutorialPage(int pageNr){
		System.out.println("tutorialIndexEntries " + tutorialIndexEntries);
		int realPageID = pageNr%10;
		if (realPageID > tutorialIndexEntries)
            realPageID = 0;
        else if (realPageID < 0)
            realPageID = tutorialIndexEntries;

		try {
			readPage(realPageID);
		} catch (IOException e) {
			e.printStackTrace();
		}
		JSONObject envelope = new JSONObject();
		envelope.put("Args", readPage);
		Presenter.getInstance().getTutorialPresenter().displayTutorialPage(envelope);
	}

	public void onFetchNodePage(int pageNr, GraphNode node){
		String succesorInfo = "", predeccessorInfo = "";
		if (node.getSucceessor() != null)
			succesorInfo = "Successor: " + node.getSuccessorName();
		if (node.getPredecessor() != null)
			predeccessorInfo = "Predecessor: " + node.getPredeccessorName();

		JSONObject envelope = new JSONObject();
		JSONObject data = new JSONObject();
		data.put("nr", pageNr);
		data.put("sub0", new JSONArray().put(node.getConcatenatedDescription()));

		if ((!succesorInfo.equals("")) || (!predeccessorInfo.equals(""))) {
			data.put("sub1", new JSONArray().
				put(predeccessorInfo).put(succesorInfo));
		}
		data.put("img", node.getTexturePath());
		data.put("link", new JSONArray());
		envelope.put("Args", data);
		Presenter.getInstance().getTutorialPresenter().displayTutorialPage(envelope);
	}

	public void onFetchBuildingPage(int pageNr){
		int realPageID = pageNr%10;
		if (realPageID > buildingsIndex.size()-1)
            realPageID = 0;
        else if (realPageID < 0)
            realPageID = buildingsIndex.size()-1;

		String name = buildingsIndex.get(realPageID);
		GraphNode node = graphsHolder.getBuildingNode(name);
		System.out.println("["+node.getConcatenatedDescription()+"]");
		onFetchNodePage(pageNr, node);	
	}
	public void onFetchResourcePage(int pageNr){
		int realPageID = pageNr%10;
		if (realPageID > resourcesIndex.size()-1)
            realPageID = 0;
        else if (realPageID < 0)
            realPageID = resourcesIndex.size()-1;

		String name = resourcesIndex.get(realPageID);
		GraphNode node = graphsHolder.getResourceNode(name);
		System.out.println(node.getConcatenatedDescription());
		onFetchNodePage(pageNr, node);
	}
	public void onFetchDwellerPage(int pageNr){
		int realPageID = pageNr%10;
		if (realPageID > dwellersIndex.size()-1)
            realPageID = 0;
        else if (realPageID < 0)
            realPageID = dwellersIndex.size()-1;

		String name = dwellersIndex.get(realPageID);
		GraphNode node = graphsHolder.getDwellerNode(name);
		System.out.println(node.getConcatenatedDescription());
		onFetchNodePage(pageNr, node);
	}

}

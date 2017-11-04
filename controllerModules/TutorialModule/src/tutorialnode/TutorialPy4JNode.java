package tutorialnode;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

import hintsender.HintSender;
import org.json.JSONObject;
import org.json.JSONTokener;

import model.DependenciesRepresenter;
import controlnode.DispatchCenter;
import controlnode.SocketNode;
import utils.DisposingUtils;

import py4jmediator.Presenter;
import controlnode.Py4JNode;
import py4jmediator.*;

public class TutorialPy4JNode extends Py4JNode implements TutorialPresenter.OnTutorialPresenterCalled{

	private JSONObject readPage;
	private BufferedReader tutorialReader;
	private HintSender hintSender;
	private Map<Integer, String> tutorialIndex;

	public TutorialPy4JNode(DependenciesRepresenter dr, DispatchCenter dispatchCenter, String nodeName) {
		super(dr, dispatchCenter, nodeName);
		readPage = new JSONObject("{}");
		hintSender = new HintSender(this, dispatchCenter.getEventBus());
		tutorialIndex = new HashMap<Integer, String>();
	}


	/*
	 * (non-Javadoc)
	 * @see controlnode.Node#parseCommand(java.lang.String, java.lang.String[])
	 * returns - output stream understandable to the current entity in the view layer (here TutorialView)
	 */

	public String getHints(){
		//TODO, actual hints and synchronized block
		return "hints";
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
	public void atStart() { //raczej ok
		TutorialPresenter tutorialPresenter = Presenter.getInstance().getTutorialPresenter();
		tutorialPresenter.setOnTutorialPresenterCalled(this);
		tutorialPresenter.displayTutorial();

		JSONObject graphs = dr.getGraphsHolder().displayAllGraphs();
		JSONObject envelope = new JSONObject();
			envelope.put("To","Tutorial");
			envelope.put("Operation","FetchGraphs");
			envelope.put("Args", graphs);
			//sender.pushStream(envelope);
		Presenter.getInstance().getTutorialPresenter().displayDependenciesGraph(envelope);

		//fetch tutorialIndex
		String line;
		String page = "";
			tutorialIndexReader = new BufferedReader(new FileReader ("resources\\Tutorial\\tutorialIndex.json"));
			while ((line = tutorialIndexReader.readLine()) != null) {
				System.out.println("line = " + line);
				page = page.concat(line); 
			}
			tutorialIndexReader.close();

			page = page.replaceAll("[\\p{Cc}\\p{Cf}\\p{Co}\\p{Cn}]", "?");
			System.out.println("Pure string: " + page);
			readPage = new JSONObject(page);
			System.out.println("Read page:" + readPage.toString());
		//handle tutorialIndex to python view
	}

	@Override
	protected void onLoop() {

	}


	@Override
	public void atExit() { //ok
		Presenter.getInstance().getTutorialPresenter().setOnTutorialPresenterCalled(null);	
	}


	@Override
	public void atUnload() { //ok
		hintSender.atUnload();
	}

	@Override
	public void onReturnToMenu(){ //??
		moveTo("GameMenuNode");
	}

	@Override
	public void onFetchTutorialPage(int pageNr){ //ok
		try {
				readPage(pageNr);
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			JSONObject envelope = new JSONObject();
			envelope.put("To","Tutorial");
			envelope.put("Operation","FetchPage");
			JSONObject json = new JSONObject();
			json.put("Page", readPage);
			envelope.put("Args", json);
	//		return envelope.toString();
			Presenter.getInstance().getTutorialPresenter().displayTutorialPage(envelope);
	}

}

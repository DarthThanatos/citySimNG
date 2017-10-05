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

public class TutorialNode extends SocketNode{

	private JSONObject readPage;
	private BufferedReader tutorialReader;
	private HintSender hintSender;

	public TutorialNode(DependenciesRepresenter dr, DispatchCenter dispatchCenter, String nodeName) {
		super(dr, dispatchCenter, nodeName);
		readPage = new JSONObject("{}");
		hintSender = new HintSender(this, dispatchCenter.getEventBus());
	}


	/*
	 * (non-Javadoc)
	 * @see controlnode.Node#parseCommand(java.lang.String, java.lang.String[])
	 * returns - output stream understandable to the current entity in the view layer (here TutorialView)
	 */
	@Override
	public String parseCommand(String command, JSONObject args) {
		if (command.equals("RequestPage")){
			System.out.println("Tutorial: Received RequestPage");
			int pageID = args.getInt("PageID");
			System.out.println("Tutorial: PageID = " + pageID);
			try {
				readPage(pageID);
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
			return envelope.toString();
		}
		else{
			System.out.println("Tutorial: Received unknown message");
			return "{}";//tu otrzymuje wezwanie wyslania strony i podstrony(?)
		} 
	}

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
			/*JSONObject readPage = (JSONObject) new JSONTokener(page).nextValue();
			String readPageString = readPage.toString();
			if (readPageString == null){
				System.out.println("Something went wrong!");
				throw new NullPointerException();
			}*/
			System.out.println("Read page:" + readPage.toString());
	}


	@Override
	public void atStart() {
		JSONObject graphs = dr.getGraphsHolder().displayAllGraphs();
		JSONObject envelope = new JSONObject();
			envelope.put("To","Tutorial");
			envelope.put("Operation","FetchGraphs");
			envelope.put("Args", graphs);
			sender.pushStream(envelope);
	}


	@Override
	public void atExit() {
		// TODO Auto-generated method stub
		
	}


	@Override
	public void atUnload() {
		hintSender.atUnload();
	}

}

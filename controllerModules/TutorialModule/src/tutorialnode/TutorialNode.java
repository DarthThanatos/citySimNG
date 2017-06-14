package tutorialnode;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

import org.json.JSONObject;
import org.json.JSONTokener;

import model.DependenciesRepresenter;
import controlnode.DispatchCenter;
import controlnode.SocketNode;

public class TutorialNode extends SocketNode{

	private String page;
	private BufferedReader tutorialReader;
	public TutorialNode(DependenciesRepresenter dr, DispatchCenter dispatchCenter, String nodeName) {
		super(dr, dispatchCenter, nodeName);
		page = "";
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
			json.put("Page", page);
			envelope.put("Args", json);
			return envelope.toString();
		}
		else{
			System.out.println("Tutorial: Received unknown message");
			return "{}";//tu otrzymuje wezwanie wyslania strony i podstrony(?)
		} 
	}



	public void readPage(int pageID) throws IOException{
		String line;
			tutorialReader = new BufferedReader(new FileReader ("resources\\Tutorial\\page"+pageID+".json"));
			while ((line = tutorialReader.readLine()) != null) {
				System.out.println("line = " + line);
				page = page.concat(line); 
			}

			System.out.println("Pure string: " + page);
			JSONObject readPage = (JSONObject) new JSONTokener(page).nextValue();
			String readPageString = readPage.toString();
			if (readPageString == null){
				System.out.println("Something went wrong!");
				throw new NullPointerException();
			}
			System.out.println("Read page:" + readPageString);
	}


	@Override
	public void atStart() {
		// TODO Auto-generated method stub
		
	}


	@Override
	public void atExit() {
		// TODO Auto-generated method stub
		
	}


	@Override
	public void atUnload() {
		// TODO Auto-generated method stub
		
	}

}

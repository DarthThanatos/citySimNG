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
		page = null;;
	}


	/*
	 * (non-Javadoc)
	 * @see controlnode.Node#parseCommand(java.lang.String, java.lang.String[])
	 * returns - output stream understandable to the current entity in the view layer (here TutorialView)
	 */
	@Override
	public String parseCommand(String command, JSONObject args) {
		if (command.equals("RequestPage")){
			int pageID = args.getInt("PageID");
			try {
				readPage(pageID);
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			JSONObject envelope = new JSONObject();
			envelope.put("To","Tutorial");
			envelope.put("Operation","FetchPage");
			envelope.put("Page", page);
			return envelope.toString();
		}
		else 
			return "{}";//tu otrzymuje wezwanie wyslania strony i podstrony(?)
	}



	public void readPage(int pageID) throws IOException{
		String line;
			tutorialReader = new BufferedReader(new FileReader ("resources\\Tutorial\\page"+page+".json"));
			while ((line = tutorialReader.readLine()) != null) {
				page.concat(line); 
			}
			//check if it's a proper json
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

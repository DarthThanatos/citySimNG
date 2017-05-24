package rankingnode;

import java.util.ArrayList;
import java.util.HashMap;

import java.io.BufferedReader;
import java.io.FileReader;

import org.json.JSONObject;

import model.DependenciesRepresenter;
import ranking.User;
import controlnode.DispatchCenter;
import controlnode.SocketNode;

public class RankingNode extends SocketNode {

	private HashMap<String, User> users;
	private BufferedReader csvReader;
	
	public RankingNode(DependenciesRepresenter dr, DispatchCenter dispatchCenter, String nodeName){
		super(dr, dispatchCenter, nodeName);
		
		users = new HashMap<String, User>();
		
		
	}

	private void sendData(){
		JSONObject envelope = new JSONObject();
		envelope.put("To","Ranking");
		envelope.put("Operation","FetchList");
		JSONObject allArgs = new JSONObject();
		for (String s : users.keySet()){
			JSONObject json = new JSONObject();
			User currUser = users.get(s);
			json.put("userName", s);
			json.put("money", currUser.getMoney());
			json.put("nrOfGames", currUser.getNrOfGames());
			allArgs.put("list", json);
		}

		envelope.put("Args", allArgs);
		
		sender.pushStream(envelope); //linijka generujaca exception

	}
	
	private static User crunchifyCSVtoArrayList(String crunchifyCSV) {
		ArrayList<String> result = new ArrayList<String>();
		
		if (crunchifyCSV != null) {
			String[] splitData = crunchifyCSV.split("\\s*,\\s*");
			for (int i = 0; i < splitData.length; i++) {
				if (!(splitData[i] == null) || !(splitData[i].length() == 0)) {
					result.add(splitData[i].trim());
				}
			}
		}
		String name = result.get(0);
		double money = Double.parseDouble(result.get(1));
		int nrOfGames = Integer.parseInt(result.get(2));
		return new User(name, money, nrOfGames);
	}

	@Override
	public String parseCommand(String command, JSONObject args) {
		return "{}";
	}


	@Override
	public void atStart() {
		String line;
		try {
			csvReader = new BufferedReader(new FileReader ("resources\\TextFiles\\users.csv"));
			while ((line = csvReader.readLine()) != null) {
				System.out.println("Raw CSV data: " + line);
				User currUser = crunchifyCSVtoArrayList(line); 
				users.put(currUser.getName(), currUser);
			}
			sendData();
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
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

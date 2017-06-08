package mapnode;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import controlnode.SocketStreamSender;
import model.DependenciesRepresenter;

public class Dwellers {
	private int currDwellersAmount = 0;
	private int currDwellersMaxAmount = 5;
	private List<Dweller> allDwellers = new ArrayList();
	private SocketStreamSender sender;
	private final String relativeTexturesPath = "resources\\Textures\\";
	
	public Dwellers(SocketStreamSender sender, DependenciesRepresenter dr){
		//allDwellers = (List<Dweller>) dr.getModuleData("allDwellers");
		Dweller d1 = new Dweller();
		d1.setName("Zbychu");
		d1.setPredecessor("");
		d1.setSuccessor("");
		d1.setTexturePath(relativeTexturesPath + "dweller.jpg");
		Map c = new HashMap();
		c.put("Wood", 5);
		d1.setConsumes(c);
		allDwellers.add(d1);
		this.sender = sender;
	}
	
	public int getCurrDwellersAmount() {
		return currDwellersAmount;
	}

	public void setCurrDwellersAmount(int currDwellersAmount) {
		this.currDwellersAmount = currDwellersAmount;
	}

	public int getCurrDwellersMaxAmount() {
		return currDwellersMaxAmount;
	}

	public void setCurrDwellersMaxAmount(int currDwellersMaxAmount) {
		this.currDwellersMaxAmount = currDwellersMaxAmount;
	}

	public List<Dweller> getAllDewellers() {
		return allDwellers;
	}

	public void setAllDewellers(List<Dweller> allDewellers) {
		this.allDwellers = allDewellers;
	}
}

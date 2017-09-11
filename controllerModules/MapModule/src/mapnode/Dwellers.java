package mapnode;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import controlnode.SocketStreamSender;
import entities.Dweller;
import model.DependenciesRepresenter;

public class Dwellers {
	private int currDwellersAmount = 0;
	private int currDwellersMaxAmount = 5;
	private List<Dweller> allDwellers = new ArrayList();
	private final String relativeTexturesPath = "resources\\Textures\\";
	
	Dwellers(DependenciesRepresenter dr){
		allDwellers = (List<Dweller>) dr.getModuleData("allDwellers");
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

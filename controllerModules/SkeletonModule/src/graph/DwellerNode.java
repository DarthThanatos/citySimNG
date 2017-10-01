package graph;

import entities.Dweller;

public class DwellerNode extends GraphNode{

	private Dweller dweller;
	
	public DwellerNode(Dweller dweller) {
		this.dweller = dweller;
	}

	@Override
	public String getSuccessorName() {
		return dweller.getSuccessor();
	}

	@Override
	public String getPredeccessorName() {
		return dweller.getPredecessor();
	}

	@Override
	public String getConcatenatedDescription() {
		return dweller.toString();
	}

	@Override
	public String getTexturePath() {
		return dweller.getTexturePath();
	}

	@Override
	public String getName() {
		return dweller.getName();
	}

}

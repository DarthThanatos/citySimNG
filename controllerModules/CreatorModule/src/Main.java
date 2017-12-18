import constants.Consts;
import controlnode.DispatchCenter;
import creatornode.CreatorPy4JNode;
import model.DependenciesRepresenter;

import java.util.HashMap;
import java.util.Random;

public class Main {
	
	public static void main(String [] args){
//		DefaultDepTest.createDefaultDependencies();
		//GraphTutorial.main(args);
//		GraphTest.dependenciesCycleDetectionTest();
		DispatchCenter dispatchCenter = new DispatchCenter();
		CreatorPy4JNode creatorPy4JNode = new CreatorPy4JNode(dispatchCenter, "Creator");

		HashMap<String, DependenciesRepresenter> representers = (HashMap<String, DependenciesRepresenter>) dispatchCenter
				.getDispatchData(Consts.LOADER_MODULE, Consts.DEPENDENCIES_REPRESENTERS);

		String[] descSentences = representers.get("Stronghold").getGraphsHolder().getRandomBuilding().getDescription().split("\\.");
		System.out.println( descSentences[Math.abs(new Random().nextInt()) % descSentences.length] + ".");
	}
}

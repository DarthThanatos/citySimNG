package monter;

import controlnode.Node;
import org.junit.Before;
import org.junit.Test;

import java.util.ArrayList;

import static org.junit.Assert.*;

public class BaseMonterTest {

    private Node mainMenuNode;

    @Before
    public void setup(){
        SystemMonter monter  = new BaseMonter(
                "..\\..\\resources\\injectFiles\\mainInject.txt",
                System.getProperty("user.dir") + "\\.."
        );
        ArrayList<String> modulesNamesList = new ArrayList<>();
        mainMenuNode = monter.mount(modulesNamesList);
    }

    @Test
    public void testStartsAtMainMenu(){
        assertEquals("MainMenuNode", mainMenuNode.getNodeName());
    }

    @Test
    public void testSystemStructure(){
        assertNotNull(mainMenuNode.getNeighbour("CreatorNode"));
        assertNotNull(mainMenuNode.getNeighbour("LoaderNode"));
        assertEquals(
                "MainMenuNode",
                mainMenuNode
                        .getNeighbour("CreatorNode")
                        .getParent()
                        .getNodeName()
        );
        assertEquals(
                "MainMenuNode",
                mainMenuNode
                        .getNeighbour("LoaderNode")
                        .getParent()
                        .getNodeName()
        );
        assertNull(
                mainMenuNode
                        .getNeighbour("LoaderNode")
                        .getNeighbour("GameMenuNode")
        ); //it ascertains that no game was mounted at this point
        assertNotNull(
                mainMenuNode
                        .getNeighbour("CreatorNode")
                        .getNeighbour("MainMenuNode")
        );
        assertNotNull(
                mainMenuNode
                        .getNeighbour("LoaderNode")
                        .getNeighbour("MainMenuNode")
        );
    }

}
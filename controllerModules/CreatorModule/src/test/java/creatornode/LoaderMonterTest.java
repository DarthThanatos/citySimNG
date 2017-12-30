package creatornode;

import constants.Consts;
import controlnode.DispatchCenter;
import controlnode.Node;
import model.DependenciesRepresenter;
import monter.LoaderMonter;
import monter.SystemMonter;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mock;

import java.util.ArrayList;
import java.util.HashMap;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertNull;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

public class LoaderMonterTest {

    @Mock
    private DispatchCenter dispatchCenter;

    private Node gameMenuNode;

    @Before
    public void setup(){
        dispatchCenter = mock(DispatchCenter.class);
        HashMap<String, DependenciesRepresenter> representers = new HashMap<>();
        when(dispatchCenter.getDispatchData(Consts.LOADER_MODULE, Consts.DEPENDENCIES_REPRESENTERS)).thenReturn(representers);
        new CreatorPy4JNode(dispatchCenter, "Creator",
                "..\\..\\resources\\sysFiles\\defaultDependencies\\");

        SystemMonter monter  = new LoaderMonter(
                "..\\..\\resources\\injectFiles\\loaderInject.txt",
                dispatchCenter,
                representers.get("Moon"),
                System.getProperty("user.dir") + "\\.."
        );
        
        ArrayList<String> modulesNamesList = new ArrayList<>();
        gameMenuNode = monter.mount(modulesNamesList);
    }

    @Test
    public void testStartsAtGameMenu(){
        assertEquals("GameMenuNode", gameMenuNode.getNodeName());
    }

    @Test
    public void testSystemStructure(){
        assertNotNull(gameMenuNode.getNeighbour("MapNode"));
        assertNotNull(gameMenuNode.getNeighbour("TutorialNode"));
        assertNotNull(gameMenuNode.getNeighbour("ExchangeNode"));
        assertEquals(
                "GameMenuNode",
                gameMenuNode
                        .getNeighbour("MapNode")
                        .getParent()
                        .getNodeName()
        );
        assertEquals(
                "GameMenuNode",
                gameMenuNode
                        .getNeighbour("TutorialNode")
                        .getParent()
                        .getNodeName()
        );
        assertEquals(
                "GameMenuNode",
                gameMenuNode
                        .getNeighbour("ExchangeNode")
                        .getParent()
                        .getNodeName()
        );

        assertNotNull(
                gameMenuNode
                        .getNeighbour("MapNode")
                        .getNeighbour("GameMenuNode")
        );
        assertNotNull(
                gameMenuNode
                        .getNeighbour("TutorialNode")
                        .getNeighbour("GameMenuNode")
        );
        assertNotNull(
                gameMenuNode
                        .getNeighbour("ExchangeNode")
                        .getNeighbour("GameMenuNode")
        );
    }
}
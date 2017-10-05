package hintsender;
import com.google.common.eventbus.EventBus;
import io.reactivex.Observable;
import io.reactivex.disposables.Disposable;
import io.reactivex.schedulers.Schedulers;
import model.TutorialHintEvent;
import tutorialnode.TutorialNode;
import utils.DisposingUtils;

import java.util.concurrent.TimeUnit;

public class HintSender {
    private final TutorialNode tutorialNode;
    private Disposable hintsSendingDisposable;
    private EventBus eventBus;

    public HintSender(TutorialNode tutorialNode, EventBus eventBus){
        this.eventBus  = eventBus;
        this.tutorialNode = tutorialNode;
        startSending();

    }

    private void startSending(){
        //TODO - more sophisticated algorithm of calculating when hint should be sent needed
        hintsSendingDisposable = Observable.interval(5, TimeUnit.SECONDS)
                .subscribeOn(Schedulers.newThread())
                .forEachWhile(this::notInterrupted, Throwable::printStackTrace);
    }

    private boolean notInterrupted(Long aLong) {
        System.out.println("Sending event to map module");
        eventBus.post(new TutorialHintEvent(tutorialNode.getHints()));
        return true;
    }

    public void atUnload(){
        System.out.println("stopping sending hints");
        DisposingUtils.dispose(hintsSendingDisposable);
    }
}

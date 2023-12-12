from SingeltonAppManager.AppManager import app
import time 
import threading

#Subject: this is the core of the pattern, since when changed it needs to communicate to the other places 
# fetch tracks is responsible for fetching and storing track info 
# subject fetches tracks and keeps a list of the observers 
class TracksSubject: 
    def __init__(self, sp):
        self._observers = []
        self.tracks = []
        self._running = False
        self.sp = sp #spotify client instance 

    def register_observer(self, observer):
        self._observers.append(observer)

    def notify_observers(self):
        for observer in self._observers:
          observer.update(self._tracks) 

    def fetch_tracks(self):
        tracks = self.sp.current_user_saved_tracks()
        self._tracks = tracks
        self.notify_observers() 

    def start_fetching(self):
        self._running = True
        while self._running:
          self.fetch_tracks()
          time.sleep(30)

    def stop_fetching(self):
        self._running = False

    def run(self):
        fetching_thread = threading.Thread(target=self.start_fetching)
        fetching_thread.start()

# The observer is a class that defines the update method which is called by the subject to notify the obserevs of any chance 
# concerete implemetnation of the observer are the actual objets that are insteresed in the state of the subject and react to the changes
# Track info Observer, when it receives the notification (update) the process the new track data 
# this is what wishes to be updated changes in data 
# the subject will call the update methosd, and observers register with subjects 

class trackInfoObserver:
    def __init__(self):
        self.tracks = []

    def update(self, tracks):
        #print("YALLLL", tracks)
        self.tracks = tracks  # Update the stored tracks
        
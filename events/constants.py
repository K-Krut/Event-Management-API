EVENT_STATUSES = ['Draft', 'Active', 'Upcoming', 'Ongoing', 'Canceled', 'Finished']
EVENT_FORMATS = ["Online", "Offline", "Hybrid"]
EVENT_TYPES = ["Conference", "Meetup", "Webinar", "Hackathon", "Lecture", "Networking", "Exhibition"]

EVENT_STATUSES_EXCLUDED_IN_LIST = ['Draft', 'Canceled']
EVENT_STATUSES_ALLOWED_FOR_CREATE = ['Draft', 'Active', 'Upcoming']
EVENT_STATUSES_NOT_EDITABLE = ['Canceled', 'Finished']

EVENT_FORMATS_WITH_REQUIRED_LOCATION = ["Offline", "Hybrid"]
EVENT_FORMATS_WITHOUT_LOCATION = ["Online"]

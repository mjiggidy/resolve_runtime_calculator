import dataclasses

@dataclasses.dataclass(frozen=True)
class TRTMainWindowOptions:

	show_nag_link:bool
	main_window_title:str
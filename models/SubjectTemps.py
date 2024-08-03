from main import *



class ObjectTemp(WindowInterface):

    # ///////////////////////////////
    # danh sách các nút text ở menu
    def TempsButtonTextWidgets(self , widgets):
        return [
             widgets.btn_banking , widgets.btn_booking ,
            widgets.btn_file_custom , widgets.btn_help , widgets.btn_hide , widgets.btn_history,
             widgets.btn_user,
            # ///////////////////////////////////////
            # button_icons
            ]
    

    # ///////////////////////////////////
    # danh sách các nút tiện ích
    def TempsButtonToolsWidgets(self , widgets):
        return [widgets.btn_refresh ,widgets.btn_delete , widgets.btn_bin ,
                widgets.btn_proxy, widgets.btn_add,widgets.btn_plan_tool]
    
    # ////////////////////////////////////
    # danh sách các nút icon menu 
    def TempsButtonIconsWidgets(self , widgets):
        return [widgets.btn_banking_icons , widgets.btn_booking_icons ,
            widgets.btn_file_custom_icons , widgets.btn_help_icons  , widgets.btn_hide_icons,
            widgets.btn_history_icons,
             widgets.btn_user_icons]
    
    def TempsComboBoxAddItems(self,window_widgets):
        return [window_widgets.combox_1 , window_widgets.combox_2 , window_widgets.combox_3,
                     window_widgets.combox_4 , window_widgets.combox_5 , window_widgets.combox_6,
                     window_widgets.combox_7 , window_widgets.combox_8 , window_widgets.combox_9,
                     window_widgets.combox_10, window_widgets.combox_11, window_widgets.combox_12,
                     window_widgets.combox_13, window_widgets.combox_14
                     ]
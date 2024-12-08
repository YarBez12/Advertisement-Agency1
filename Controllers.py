from PyQt5.QtCore import Qt

from Windows import *
from Models import *
import InitialData

class AddWindowController:
    def set_widget_state(self, widget, button, text, enabled):
        widget.setEnabled(enabled)
        button.setText(text)

    def toggle_widget(self, widget, button, add_text, remove_text):
        if widget.isEnabled():
            self.set_widget_state(widget, button, add_text, False)
        else:
            self.set_widget_state(widget, button, remove_text, True)

class AddAdvertisementWindowController(AddWindowController):
    def __init__(self, window):
        self.__window = window

    def toggle_time(self) -> None:
        self.toggle_widget(self.__window.sendDateEdit, self.__window.dateButton, "Add time", "Remove time")

    def toggle_language(self) -> None:
        self.toggle_widget(self.__window.languageComboBox, self.__window.languageButton, "Add language",
                           "Remove language")

    def toggle_campaign(self) -> None:
        self.toggle_widget(self.__window.campaignComboBox, self.__window.campaignButton, "Add campaign",
                           "Remove campaign")

    def toggle_platform(self) -> None:
        self.toggle_widget(self.__window.platformComboBox, self.__window.platformButton, "Add platform",
                           "Remove platform")

    def update_attachment_line_edit(self, file_path):
        if file_path:
            self.__window.attachmentLineEdit.setText(file_path)

    def select_max_id_from_table(self) -> int:

        if not InitialData.Advertisements.get_items():
            return -1
        try:
            max_id = max(ad.advertisement_id for ad in InitialData.Advertisements.get_items())
            return max_id
        except ValueError:
            return -1

    def validate_window(self):
        advertisement_topic = self.__window.topicLineEdit.text().strip()
        if not advertisement_topic:
            return "Please fill in the advertisement topic"
        try:
            self.get_data()
        except Exception as e:
            return str(e)
        return ""

    def get_data(self) -> Optional[Advertisement]:
        send_date_qdate = self.__window.sendDateEdit.date()
        campaign_name = self.__window.campaignComboBox.currentText().strip() if self.__window.campaignComboBox.isEnabled() else None
        if campaign_name is not None:
            campaign = next((c for c in InitialData.Campaigns.get_items() if c.campaign_name == campaign_name), None)
            campaign_id = campaign.campaign_id
        else:
            campaign_id = None
        platform_name = self.__window.platformComboBox.currentText().strip() if self.__window.platformComboBox.isEnabled() else None
        if platform_name:
            platform = next((p for p in InitialData.MediaPlatforms.get_items() if p.platform_name == platform_name),
                            None)
            platform_id = platform.platform_id
        else:
            platform_id = None
        text = self.__window.textLineEdit.text().strip()
        attachment = self.__window.attachmentLineEdit.text().strip()
        return Advertisement(
            advertisement_id=int(self.__window.idLineEdit.text().strip()),
            text=text if text else None,
            format=self.__window.formatComboBox.currentText(),
            send_time=datetime.combine(send_date_qdate.toPyDate(),
                                       datetime.min.time()) if self.__window.sendDateEdit.isEnabled() else None,
            topic=self.__window.topicLineEdit.text().strip(),
            language=self.__window.languageComboBox.currentText() if self.__window.languageComboBox.isEnabled() else None,
            attachment=attachment if attachment else None,
            clicks=int(
                self.__window.clicksLineEdit.text().strip()) if self.__window.clicksLineEdit.text().strip() else None,
            views=int(
                self.__window.viewsLineEdit.text().strip()) if self.__window.viewsLineEdit.text().strip() else None,
            campaign_id=campaign_id,
            platform_id=platform_id
        )

    def reset_data(self):
        max_id = self.select_max_id_from_table()
        self.__window.idLineEdit.setText(str(max_id + 1))
        self.__window.textLineEdit.clear()
        self.__window.formatComboBox.setCurrentIndex(0)
        self.__window.sendDateEdit.setDate(QDate.currentDate().addMonths(1))
        self.__window.sendDateEdit.setEnabled(True)
        self.__window.topicLineEdit.clear()
        self.__window.languageComboBox.setCurrentIndex(0)
        self.__window.attachmentLineEdit.clear()
        self.__window.clicksLineEdit.clear()
        self.__window.viewsLineEdit.clear()
        self.__window.campaignComboBox.setCurrentIndex(0)
        self.__window.platformComboBox.setCurrentIndex(0)
        self.__window.sendDateEdit.setEnabled(False)
        self.__window.dateButton.setText("Add date")
        self.__window.languageComboBox.setEnabled(False)
        self.__window.languageButton.setText("Add language")
        self.__window.campaignComboBox.setEnabled(False)
        self.__window.campaignButton.setText("Add campaign")
        self.__window.platformComboBox.setEnabled(False)
        self.__window.platformButton.setText("Add platform")

    def set_data(self, advertisement: Advertisement) -> None:
        self.__window.idLineEdit.setText(str(advertisement.advertisement_id))
        self.__window.textLineEdit.setText(advertisement.text or "")
        self.__window.formatComboBox.setCurrentText(advertisement.format or "")
        self.set_widget_state(self.__window.sendDateEdit, self.__window.dateButton,
                                "Remove date" if advertisement.send_time else "Add date", bool(advertisement.send_time))
        if advertisement.send_time is not None:
            self.__window.sendDateEdit.setDate(advertisement.send_time)
        self.__window.topicLineEdit.setText(advertisement.topic or "")
        self.set_widget_state(self.__window.languageComboBox, self.__window.languageButton,
                                "Remove language" if advertisement.language else "Add language",
                                bool(advertisement.language))
        if advertisement.language is not None:
            self.__window.languageComboBox.setCurrentText(advertisement.language)
        self.__window.attachmentLineEdit.setText(advertisement.attachment or "")
        self.__window.clicksLineEdit.setText(str(advertisement.clicks) if advertisement.clicks is not None else "")
        self.__window.viewsLineEdit.setText(str(advertisement.views) if advertisement.views is not None else "")
        campaign = next((c for c in InitialData.Campaigns.get_items() if c.campaign_id == advertisement.campaign_id),
                        None)
        self.set_widget_state(self.__window.campaignComboBox, self.__window.campaignButton,
                                "Remove campaign" if campaign else "Add campaign", bool(campaign))
        if campaign is not None:
            self.__window.campaignComboBox.setCurrentText(campaign.campaign_name)
        platform = next(
            (p for p in InitialData.MediaPlatforms.get_items() if p.platform_id == advertisement.platform_id),
            None)
        self.set_widget_state(self.__window.platformComboBox, self.__window.platformButton,
                                "Remove platform" if platform else "Add platform", bool(platform))
        if platform:
            self.__window.platformComboBox.setCurrentText(platform.platform_name)

    def set_campaign_name(self, campaign_name):
        self.__window.campaignComboBox.setCurrentText(str(campaign_name))
        self.__window.campaignComboBox.setEnabled(False)

    def set_platform_name(self, platform_name):
        self.__window.platformComboBox.setCurrentText(str(platform_name))
        self.__window.platformComboBox.setEnabled(False)


class AddCampaignWindowController(AddWindowController):
    def __init__(self, window):
        self.__window = window

    def toggle_start_date(self) -> None:
        self.toggle_widget(self.__window.startDateEdit, self.__window.startDateButton, "Add date", "Remove date")

    def toggle_end_date(self) -> None:
        self.toggle_widget(self.__window.endDateEdit, self.__window.endDateButton, "Add date",
                           "Remove date")

    def toggle_budget(self) -> None:
        self.toggle_widget(self.__window.budgetSpinBox, self.__window.budgetButton, "Add budget", "Remove budget")

    def toggle_budget_allocation(self) -> None:
        self.toggle_widget(self.__window.budgetAllocationSpinBox, self.__window.budgetAllocationButton, "Add budget",
                           "Remove budget")



    def populate_combobox(combobox, items, attribute):
        combobox.clear()
        combobox.addItems([getattr(item, attribute) for item in items if getattr(item, attribute, None)])

    def select_max_id_from_table(self) -> int:
        if not InitialData.Campaigns.get_items():
            return -1
        try:
            max_id = max(c.campaign_id for c in InitialData.Campaigns.get_items())
            return max_id
        except ValueError:
            return -1

    def validate_window(self):
        campaign_goal = self.__window.goalLineEdit.text().strip()
        if not campaign_goal:
            return "Please fill in the campaign goal"
        try:
            self.get_data()
        except Exception as e:
            return str(e)
        return ""

    def get_data(self) -> Optional[Campaign]:
        start_date_qdate = self.__window.startDateEdit.date()
        end_date_qdate = self.__window.endDateEdit.date()
        campaign_name = self.__window.nameLineEdit.text().strip()
        return Campaign(
            campaign_id=int(self.__window.idLineEdit.text().strip()),
            campaign_name=campaign_name if campaign_name else None,
            start_date=datetime.combine(start_date_qdate.toPyDate(),
                                        datetime.min.time()) if self.__window.startDateEdit.isEnabled() else None,
            end_date=datetime.combine(end_date_qdate.toPyDate(),
                                      datetime.min.time()) if self.__window.endDateEdit.isEnabled() else None,
            goal=self.__window.goalLineEdit.text().strip(),
            budget=self.__window.budgetSpinBox.value() if self.__window.budgetSpinBox.isEnabled() else None,
            company_name=self.__window.companyComboBox.currentText(),
        )

    def reset_data(self) -> None:
        max_id = self.select_max_id_from_table()
        self.__window.idLineEdit.setText(str(max_id + 1))
        self.__window.nameLineEdit.setPlaceholderText(f"Campaign #{max_id + 1}")
        self.__window.startDateEdit.setDate(QDate.currentDate())
        self.__window.endDateEdit.setDate(QDate.currentDate().addYears(5))
        self.__window.startDateEdit.setEnabled(False)
        self.__window.endDateEdit.setEnabled(False)
        self.__window.budgetSpinBox.setEnabled(False)
        self.__window.budgetAllocationSpinBox.setEnabled(False)
        self.__window.startDateButton.setText("Add Date")
        self.__window.endDateButton.setText("Add Date")
        self.__window.budgetButton.setText("Add budget")
        self.__window.budgetAllocationButton.setText("Add budget")
        self.__window.goalLineEdit.clear()
        self.__window.budgetSpinBox.setValue(1000)
        self.__window.companyComboBox.setCurrentIndex(0)

    def set_data(self, campaign: Campaign) -> None:
        self.__window.idLineEdit.setText(str(campaign.campaign_id))
        self.__window.nameLineEdit.setText(campaign.campaign_name or "")
        self.set_widget_state(self.__window.startDateEdit, self.__window.startDateButton,
                              "Remove date" if campaign.start_date else "Add date",
                              bool(campaign.start_date))
        if campaign.start_date:
            self.__window.startDateEdit.setDate(campaign.start_date)
        self.set_widget_state(self.__window.endDateEdit, self.__window.endDateButton,
                              "Remove date" if campaign.end_date else "Add date",
                              bool(campaign.end_date))
        if campaign.end_date:
            self.__window.endDateEdit.setDate(campaign.end_date)
        self.set_widget_state(self.__window.budgetSpinBox, self.__window.budgetButton,
                              "Remove budget" if campaign.budget else "Add budget",
                              bool(campaign.budget))
        if campaign.budget is not None:
            self.__window.budgetSpinBox.setValue(campaign.budget)
        self.__window.goalLineEdit.setText(campaign.goal or "")
        self.__window.companyComboBox.setCurrentText(campaign.company_name or "")

    def set_budget_allocation(self, value):
        self.set_widget_state(self.__window.budgetAllocationSpinBox, self.__window.budgetAllocationButton,
                              "Remove budget" if value else "Add budget",
                              bool(value))
        if value is not None:
            self.budgetAllocationSpinBox.setValue(value)



class AddClientWindowController(AddWindowController):
    def __init__(self, window):
        self.__window = window


    def toggle_budget(self) -> None:
        self.toggle_widget(self.__window.budgetSpinBox, self.__window.budgetButton, "Add budget", "Remove budget")


    def validate_window(self):
        client_name = self.__window.nameLineEdit.text().strip()
        client_phone = self.__window.phoneLineEdit.text().strip()
        client_email = self.__window.emailLineEdit.text().strip()
        client_password = self.__window.passwordLineEdit.text().strip()
        if not client_name:
            return "Please fill in the company name"
        if not client_phone:
            return "Please fill in the phone"
        if not client_email:
            return "Please fill in the email"
        if not client_password:
            return "Please fill in the password"
        try:
            self.get_data()
        except Exception as e:
            return str(e)
        return ""

    def get_data(self) -> Optional[Client]:
        address = self.__window.addressLineEdit.text().strip()
        return Client(
            company_name=self.__window.nameLineEdit.text().strip(),
            phone=self.__window.phoneLineEdit.text().strip(),
            email=self.__window.emailLineEdit.text().strip(),
            password=self.__window.passwordLineEdit.text().strip(),
            address=address if address else None,
            type=self.__window.typeComboBox.currentText(),
            business_area=self.__window.areaComboBox.currentText(),
            available_budget=self.__window.budgetSpinBox.value() if self.__window.budgetSpinBox.isEnabled() else None
        )

    def reset_data(self) -> None:
        self.__window.nameLineEdit.clear()
        self.__window.phoneLineEdit.clear()
        self.__window.emailLineEdit.clear()
        self.__window.passwordLineEdit.clear()
        self.__window.addressLineEdit.clear()
        self.__window.typeComboBox.setCurrentIndex(0)
        self.__window.areaComboBox.setCurrentIndex(0)
        self.__window.budgetSpinBox.setValue(0)
        self.__window.budgetSpinBox.setEnabled(False)
        self.__window.budgetButton.setText("Add budget")

    def set_data(self, client) -> None:
        self.__window.nameLineEdit.setText(client.company_name or "")
        self.__window.nameLineEdit.setEnabled(False)
        self.__window.phoneLineEdit.setText(client.phone or "")
        self.__window.emailLineEdit.setText(client.email or "")
        self.__window.passwordLineEdit.setText(client.password or "")
        self.__window.addressLineEdit.setText(client.address or "")
        self.__window.typeComboBox.setCurrentText(client.type or "")
        self.__window.areaComboBox.setCurrentText(client.business_area or "")
        self.set_widget_state(self.__window.budgetSpinBox, self.__window.budgetButton,
                              "Remove budget" if client.available_budget else "Add budget",
                              bool(client.available_budget))
        if client.available_budget is not None:
            self.__window.budgetSpinBox.setValue(client.available_budget)


class TablesWindowController:
    def __init__(self, window):
        self.__window = window
        self.current_data = InitialData.Clients
        self.display_data = InitialData.Clients
        self.sort_criteria = None
        self.find_criteria = None
        self.filter_criteria = None
        self.sort_key_mapping = {
            "Campaigns": {
                "By start date": lambda x: getattr(x, "start_date", None),
                "By budget": lambda x: getattr(x, "budget", None),
                "By name": lambda x: getattr(x, "campaign_name", None)
            },
            "Clients": {
                "By company name": lambda x: getattr(x, "company_name", None),
                "By type": lambda x: getattr(x, "type", None),
                "By available budget": lambda x: getattr(x, "available_budget", None)
            }
        }
        self.find_contains_functions = {
            "Campaigns": lambda: [self.find_criteria["Name"],
                                  self.find_criteria["Goal"]],
            "Clients": lambda: [self.find_criteria["Name"], self.find_criteria["Email"],
                                self.find_criteria["Phone"], self.find_criteria["Area"]]
        }
        self.find_functions_mapping = {
            "Campaigns": lambda x: {"Name": x[0], "Goal": x[1]},
            "Clients": lambda x: {"Name": x[0], "Email": x[1], "Phone": x[2], "Area": x[3]}
        }
        self.filter_functions_mapping = {
            "Advertisements": lambda x: {"Formats": x[0], "Languages": x[1], "Before date": x[2],
                                         "After date": x[3], "Minimum clicks": x[4]},
            "Audience Segments": lambda x: {"Genders": x[0], "Locations": x[1], "Devices": x[2],
                                            "Minimum age": x[3], "Maximum age": x[4]}
        }
        self.filter_functions = {
            "Advertisements": lambda: [self.filter_criteria["Formats"], self.filter_criteria["Languages"],
                                       self.filter_criteria["Before date"], self.filter_criteria["After date"],
                                       self.filter_criteria["Minimum clicks"]],
            "Audience Segments": lambda: [self.filter_criteria["Genders"], self.filter_criteria["Locations"],
                                          self.filter_criteria["Devices"], self.filter_criteria["Minimum age"],
                                          self.filter_criteria["Maximum age"]]
        }
        # self.find_criteria = {"Name": search_criteria[0], "Goal": search_criteria[1]}

        # found_items = self.current_data.find_contains(self.find_criteria["Name"],
        #                                               self.find_criteria["Goal"])
        # found_items = self.current_data.find_contains(*(self.find_contains_functions[self.current_data.get_str_models_name()]()))

    def fill_table(self, data) -> None:
        if not data:
            self.__window.dataTableWidget.clear()
            return
        headers = data[0].GetData()[0]
        related_data_map = {
            "Segment ID": {
                "map": {segment.segment_id: segment.segment_name for segment in
                        InitialData.AudienceSegments.get_items()},
                "new_header": "Segment Name",
            },
            "Platform ID": {
                "map": {platform.platform_id: platform.platform_name for platform in
                        InitialData.MediaPlatforms.get_items()},
                "new_header": "Platform Name",
            },
            "Campaign ID": {
                "map": {campaign.campaign_id: campaign.campaign_name for campaign in InitialData.Campaigns.get_items()},
                "new_header": "Campaign Name",
            },
        }
        updated_headers = [
            related_data_map[header]["new_header"] if header in related_data_map and headers.index(
                header) != 0 else header
            for header in headers
        ]
        self.__window.dataTableWidget.setRowCount(len(data))
        self.__window.dataTableWidget.setColumnCount(len(headers))
        self.__window.dataTableWidget.setHorizontalHeaderLabels(updated_headers)
        for row_ind, row_data in enumerate(data.get_items()):
            for col_ind, col_data in enumerate(row_data.GetData()[1]):
                if col_data is not None:
                    header_name = headers[col_ind]
                    if header_name in related_data_map and col_data in related_data_map[header_name][
                        "map"] and col_ind != 0:
                        display_value = related_data_map[header_name]["map"][col_data]
                    else:
                        display_value = str(col_data)
                    item = QTableWidgetItem(display_value)
                else:
                    item = QTableWidgetItem("")
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.__window.dataTableWidget.setItem(row_ind, col_ind, item)

    def update_table(self, data) -> None:
        self.current_data = data
        self.display_data = data
        self.fill_table(data)
        self.__window.databaseNameLabel.setText(data.get_str_models_name())

    def fill_table_with_edited_data(self):
        self.display_data = self.current_data
        if self.find_criteria:
            found_collection = self.current_data.find_contains(
                *(self.find_contains_functions[self.current_data.get_str_models_name()]()))
            self.display_data = found_collection
        elif self.filter_criteria:
            filter_collection = self.current_data.filter(
                *(self.filter_functions[self.current_data.get_str_models_name()]()))
            self.display_data = filter_collection
        if self.sort_criteria:
            # self.display_data = self.current_data.sort_items(self.sort_key_mapping[self.sort_criteria])
            self.display_data = self.display_data.sort_items(
                self.sort_key_mapping[self.current_data.get_str_models_name()][self.sort_criteria])
        self.fill_table(self.display_data)

    def navigate_first(self) -> None:
        if self.__window.dataTableWidget.rowCount() > 0:
            self.__window.dataTableWidget.selectRow(0)

    def navigate_previous(self) -> None:
        current_row = self.__window.dataTableWidget.currentRow()
        if current_row > 0:
            self.__window.dataTableWidget.selectRow(current_row - 1)

    def navigate_next(self) -> None:
        current_row = self.__window.dataTableWidget.currentRow()
        if current_row < self.__window.dataTableWidget.rowCount() - 1:
            self.__window.dataTableWidget.selectRow(current_row + 1)

    def navigate_last(self) -> None:
        if self.__window.dataTableWidget.rowCount() > 0:
            self.__window.dataTableWidget.selectRow(self.__window.dataTableWidget.rowCount() - 1)

    def remove_item(self, selected_row: int) -> Optional[str]:
        if selected_row == -1:
            return None

        key_value = self.__window.dataTableWidget.item(selected_row, 0).text()
        table_name = self.current_data.get_str_models_name()
        remove_item = next(
            (item for item in self.display_data.get_items() if str(item.GetData()[1][0]) == key_value),
            None
        )
        if remove_item:
            if table_name == "Clients":
                associated_campaigns = [c for c in InitialData.Campaigns.get_items() if
                                        c.company_name == remove_item.company_name]
                for campaign in associated_campaigns:
                    self._remove_campaign_dependencies(campaign)
                    InitialData.Campaigns.remove(campaign)
            elif table_name == "Campaigns":
                self._remove_campaign_dependencies(remove_item)
            elif table_name == "Media Platforms":
                self._remove_platform_dependencies(remove_item)
            elif table_name == "Audience Segments":
                self._remove_segment_dependencies(remove_item)
            self.current_data.remove(remove_item)
            if self.current_data != self.display_data:
                self.display_data.remove(remove_item)
            self.fill_table_with_edited_data()
        return key_value

    def _remove_campaign_dependencies(self, campaign):
        related_campaign_platforms = [cp for cp in InitialData.CampaignPlatforms.get_items() if
                                      cp.campaign_id == campaign.campaign_id]
        for cp in related_campaign_platforms:
            InitialData.CampaignPlatforms.remove(cp)
        related_ads = [ad for ad in InitialData.Advertisements.get_items() if ad.campaign_id == campaign.campaign_id]
        for ad in related_ads:
            ad.campaign_id = None

    def _remove_platform_dependencies(self, platform):
        related_campaign_platforms = [cp for cp in InitialData.CampaignPlatforms.get_items() if
                                      cp.platform_id == platform.platform_id]
        for cp in related_campaign_platforms:
            InitialData.CampaignPlatforms.remove(cp)
        related_segment_platforms = [sp for sp in InitialData.SegmentPlatforms.get_items() if
                                     sp.platform_id == platform.platform_id]
        for sp in related_segment_platforms:
            InitialData.SegmentPlatforms.remove(sp)
        related_ads = [ad for ad in InitialData.Advertisements.get_items() if ad.platform_id == platform.platform_id]
        for ad in related_ads:
            ad.platform_id = None

    def _remove_segment_dependencies(self, segment):
        related_segment_platforms = [sp for sp in InitialData.SegmentPlatforms.get_items() if
                                     sp.segment_id == segment.segment_id]
        for sp in related_segment_platforms:
            InitialData.SegmentPlatforms.remove(sp)
        related_users = [user for user in InitialData.Users.get_items() if user.segment_id == segment.segment_id]
        for user in related_users:
            user.segment_id = None

    def get_item_for_edit(self, selected_row: int) -> Optional[Any]:
        if selected_row == -1:
            return None

        return self.display_data.get_items()[selected_row]

    def save_item(self, data: Any, edit: bool, selected_row: Optional[int] = None) -> None:
        if edit and selected_row is not None:
            key_value = self.__window.dataTableWidget.item(selected_row, 0).text()
            current_index = next(
                (index for index, item in enumerate(self.current_data.get_items())
                 if str(item.GetData()[1][0]) == key_value),
                None
            )
            if current_index is not None:
                self.current_data.update(current_index, data)
            self.display_data.update(selected_row, data)
        else:
            self.current_data.add(data)
            # self.display_data.add(data)
        # if self.find_criteria:
        #     self.display_data = self.current_data.find_contains(self.find_criteria["Name"],
        #                                                         self.find_criteria["Goal"])
        # if self.sort_criteria:
        #     self.display_data = self.display_data.sort_items(self.sort_key_mapping[self.sort_criteria])
        # self.fill_table(self.display_data)
        self.fill_table_with_edited_data()

    def sort_table(self, sort_option):
        if sort_option in self.sort_key_mapping[self.current_data.get_str_models_name()]:
            self.display_data = self.current_data.sort_items(
                self.sort_key_mapping[self.current_data.get_str_models_name()][sort_option])
            self.sort_criteria = sort_option
            self.fill_table_with_edited_data()

    def find_items(self, search_criteria):
        found_collection = self.current_data.find_contains(*search_criteria)

        if len(found_collection) == 0:
            raise ValueError("No items found!")

        self.display_data = found_collection
        self.find_criteria = self.find_functions_mapping[self.current_data.get_str_models_name()](search_criteria)
        self.fill_table_with_edited_data()

    def filter_items(self, filter_options):
        filter_collection = self.current_data.filter(*filter_options)
        if len(filter_collection) == 0:
            raise ValueError("No items found")
        self.display_data = filter_collection
        self.filter_criteria = self.filter_functions_mapping[self.current_data.get_str_models_name()](filter_options)
        self.fill_table_with_edited_data()


class AddPlatformWindowController(AddWindowController):
    def __init__(self, window):
        self.__window = window

    def set_budget_allocation(self, value):
        self.set_widget_state(self.__window.budgetAllocationSpinBox, self.__window.budgetAllocationButton,
                              "Remove budget" if value else "Add budget",
                              bool(value))
        if value is not None:
            self.budgetAllocationSpinBox.setValue(value)



    def toggle_budget_allocation(self) -> None:
        self.toggle_widget(self.__window.budgetAllocationSpinBox, self.__window.budgetAllocationButton, "Add budget", "Remove budget")

    def toggle_type(self) -> None:
        self.toggle_widget(self.__window.typeComboBox, self.__window.typeButton, "Add type",
                           "Remove type")

    def toggle_format(self) -> None:
        self.toggle_widget(self.__window.formatComboBox, self.__window.formatButton, "Add format",
                           "Remove format")

    def toggle_size(self) -> None:
        self.toggle_widget(self.__window.audienceSpinBox, self.__window.sizeButton, "Add size",
                           "Remove size")

    def validate_window(self):
        platform_name = self.__window.nameLineEdit.text().strip()
        if not platform_name:
            return "Please fill in the platform name"
        try:
            self.get_data()
        except Exception as e:
            return str(e)

        return ""

    def select_max_id_from_table(self) -> int:

        if not InitialData.MediaPlatforms.get_items():
            return -1
        try:
            max_id = max(p.platform_id for p in InitialData.MediaPlatforms.get_items())
            return max_id
        except ValueError:
            return -1

    def get_data(self):
        return MediaPlatform(
            platform_id=int(self.__window.idLineEdit.text().strip()),
            platform_name=self.__window.nameLineEdit.text().strip(),
            platform_type=self.__window.typeComboBox.currentText().strip() if self.__window.typeComboBox.isEnabled() else None,
            main_ad_format=self.__window.formatComboBox.currentText().strip() if self.__window.formatComboBox.isEnabled() else None,
            audience_size=int(
                self.__window.audienceSpinBox.value()) if self.__window.audienceSpinBox.isEnabled() else None
        )

    def reset_data(self):
        max_id = self.select_max_id_from_table()
        self.__window.idLineEdit.setText(str(max_id + 1))
        self.__window.nameLineEdit.clear()
        self.__window.typeComboBox.setCurrentIndex(0)
        self.__window.formatComboBox.setCurrentIndex(0)
        self.__window.audienceSpinBox.setValue(0)
        self.__window.budgetAllocationSpinBox.setEnabled(False)
        self.__window.budgetAllocationButton.setText("Add budget")
        self.__window.audienceSpinBox.setEnabled(True)
        self.__window.sizeButton.setText("Add size")
        self.__window.typeComboBox.setEnabled(True)
        self.__window.typeButton.setText("Add type")
        self.__window.formatComboBox.setEnabled(True)
        self.__window.formatButton.setText("Add format")

    def set_data(self, platform: MediaPlatform) -> None:
        self.__window.idLineEdit.setText(str(platform.platform_id))
        self.__window.nameLineEdit.setText(platform.platform_name or "")
        self.set_widget_state(self.__window.typeComboBox, self.__window.typeButton,
                              "Remove type" if platform.platform_type else "Add type",
                              bool(platform.platform_type))
        if platform.platform_type is not None:
            self.__window.typeComboBox.setCurrentText(platform.platform_type)
        self.set_widget_state(self.__window.formatComboBox, self.__window.formatButton,
                              "Remove format" if platform.main_ad_format else "Add format",
                              bool(platform.main_ad_format))
        if platform.main_ad_format is not None:
            self.__window.formatComboBox.setCurrentText(platform.main_ad_format)
        self.set_widget_state(self.__window.audienceSpinBox, self.__window.sizeButton,
                              "Remove size" if platform.audience_size else "Add size",
                              bool(platform.audience_size))
        if platform.audience_size is not None:
            self.__window.audienceSpinBox.setValue(platform.audience_size)
        self.__window.typeComboBox.setCurrentText(platform.platform_type or "")
        self.__window.formatComboBox.setCurrentText(platform.main_ad_format or "")
        self.__window.audienceSpinBox.setValue(platform.audience_size if platform.audience_size is not None else 0)


class AddSegmentWindowController(AddWindowController):
    def __init__(self, window):
        self.__window = window



    def toggle_location(self) -> None:
        self.toggle_widget(self.__window.locationComboBox, self.__window.locationButton, "Add location", "Remove location")

    def toggle_device(self) -> None:
        self.toggle_widget(self.__window.deviceComboBox, self.__window.deviceButton, "Add device",
                           "Remove device")


    def validate_window(self):
        minimum_age = self.__window.minimumSpinBox.value()
        maximum_age = self.__window.maximumSpinBox.value()
        gender = self.__window.genderComboBox.currentText().strip()
        language = self.__window.languageComboBox.currentText().strip()
        if not minimum_age:
            return "Please fill in the minimum age"
        if not maximum_age:
            return "Please fill in the maximum age"
        if not gender:
            return "Please fill in the gender"
        if not language:
            return "Please fill in the language"
        try:
            self.get_data()
        except Exception as e:
            return str(e)
        return ""

    def select_max_id_from_table(self) -> int:

        if not InitialData.AudienceSegments.get_items():
            return -1
        try:
            max_id = max(s.segment_id for s in InitialData.AudienceSegments.get_items())
            return max_id
        except ValueError:
            return -1

    def get_data(self):
        segment_name = self.__window.nameLineEdit.text().strip()
        general_interest = self.__window.interestLineEdit.text().strip()
        socioeconomic_status = self.__window.statusLineEdit.text().strip()
        behavioral_characteristics = self.__window.characteristicsLineEdit.text().strip()
        return AudienceSegment(
            segment_id=int(self.__window.idLineEdit.text().strip()),
            segment_name=segment_name if segment_name else None,
            age_range=f"{self.__window.minimumSpinBox.value()}-{self.__window.maximumSpinBox.value()}",
            gender=self.__window.genderComboBox.currentText().strip(),
            location=self.__window.locationComboBox.currentText().strip() if self.__window.locationComboBox.isEnabled() else None,
            general_interest=general_interest if general_interest else None,
            socioeconomic_status=socioeconomic_status if socioeconomic_status else None,
            language=self.__window.languageComboBox.currentText().strip(),
            behavioral_characteristics=behavioral_characteristics if behavioral_characteristics else None,
            device_used=self.__window.deviceComboBox.currentText().strip() if self.__window.deviceComboBox.isEnabled() else None,
        )

    def reset_data(self):
        max_id = self.select_max_id_from_table()
        self.__window.idLineEdit.setText(str(max_id + 1))
        self.__window.nameLineEdit.clear()
        self.__window.minimumSpinBox.setValue(0)
        self.__window.maximumSpinBox.setValue(0)
        self.__window.genderComboBox.setCurrentIndex(0)
        self.__window.locationComboBox.setCurrentIndex(0)
        self.__window.languageComboBox.setCurrentIndex(0)
        self.__window.deviceComboBox.setCurrentIndex(0)
        self.__window.interestLineEdit.clear()
        self.__window.statusLineEdit.clear()
        self.__window.characteristicsLineEdit.clear()
        self.__window.locationComboBox.setEnabled(False)
        self.__window.locationButton.setText("Add location")
        self.__window.deviceComboBox.setEnabled(False)
        self.__window.deviceButton.setText("Add device")

    def set_data(self, segment: AudienceSegment) -> None:
        self.__window.idLineEdit.setText(str(segment.segment_id))
        self.__window.nameLineEdit.setText(segment.segment_name or "")
        self.__window.minimumSpinBox.setValue(int(segment.age_range[:2]))
        self.__window.maximumSpinBox.setValue(int(segment.age_range[3:]))
        self.__window.genderComboBox.setCurrentText(segment.gender or "")
        self.set_widget_state(self.__window.locationComboBox, self.__window.locationButton,
                              "Remove location" if segment.location else "Add location",
                              bool(segment.location))
        if segment.location is not None:
            self.__window.locationComboBox.setCurrentText(segment.location)
        self.__window.languageComboBox.setCurrentText(segment.language or "")
        self.set_widget_state(self.__window.deviceComboBox, self.__window.deviceButton,
                              "Remove device" if segment.device_used else "Add device",
                              bool(segment.device_used))
        if segment.device_used is not None:
            self.__window.deviceComboBox.setCurrentText(segment.device_used)
        self.__window.interestLineEdit.setText(segment.general_interest or "")
        self.__window.statusLineEdit.setText(segment.socioeconomic_status or "")
        self.__window.characteristicsLineEdit.setText(segment.behavioral_characteristics or "")


class AddUserWindowController(AddWindowController):
    def __init__(self, window):
        self.__window = window



    def toggle_date(self) -> None:
        self.toggle_widget(self.__window.lastPurchaseDateEdit, self.__window.dateButton, "Add date", "Remove date")

    def toggle_segment(self) -> None:
        self.toggle_widget(self.__window.segmentComboBox, self.__window.segmentButton, "Add segment",
                           "Remove segment")


    def validate_window(self):
        email = self.__window.emailLineEdit.text().strip()
        password = self.__window.passwordLineEdit.text().strip()
        age = self.__window.ageSpinBox.value()
        gender = self.__window.genderComboBox.currentText().strip()
        country = self.__window.countryComboBox.currentText().strip()
        account_creation_date = self.__window.createdDateEdit.text().strip()
        if not email:
            return "Please fill in the email"
        if not password:
            return "Please fill in the password"
        if not age:
            return "Please fill in the age"
        if not gender:
            return "Please fill in the gender"
        if not country:
            return "Please fill in the country"
        if not account_creation_date:
            return "Please fill in the account creation date"
        try:
            self.get_data()
        except Exception as e:
            return str(e)
        return ""

    def get_data(self) -> Optional[User]:
        segment_name = self.__window.segmentComboBox.currentText().strip() if self.__window.segmentComboBox.isEnabled() else None
        if segment_name is not None:
            segment = next((s for s in InitialData.AudienceSegments.get_items() if s.segment_name == segment_name),
                           None)
            segment_id = segment.segment_id
        else:
            segment_id = None
        return User(
            email=self.__window.emailLineEdit.text().strip(),
            password=self.__window.passwordLineEdit.text().strip(),
            age=int(self.__window.ageSpinBox.value()),
            gender=self.__window.genderComboBox.currentText().strip(),
            country=self.__window.countryComboBox.currentText().strip(),
            account_creation_date=self.__window.createdDateEdit.date().toString("yyyy-MM-dd"),
            last_purchase_date=self.__window.lastPurchaseDateEdit.date().toString(
                "yyyy-MM-dd") if self.__window.lastPurchaseDateEdit.isEnabled() else None,
            segment_id=segment_id,
        )

    def reset_data(self):
        self.__window.emailLineEdit.clear()
        self.__window.passwordLineEdit.clear()
        self.__window.ageSpinBox.setValue(0)
        self.__window.genderComboBox.setCurrentIndex(0)
        self.__window.countryComboBox.setCurrentIndex(0)
        self.__window.createdDateEdit.setDate(QDate.currentDate())
        self.__window.lastPurchaseDateEdit.clear()
        self.__window.segmentComboBox.setCurrentIndex(0)
        self.__window.lastPurchaseDateEdit.setEnabled(False)
        self.__window.dateButton.setText("Add date")
        self.__window.segmentComboBox.setEnabled(False)
        self.__window.segmentButton.setText("Add segment")

    def set_data(self, user: User) -> None:
        self.__window.emailLineEdit.setText(user.email or "")
        self.__window.emailLineEdit.setEnabled(False)
        self.__window.passwordLineEdit.setText(user.password or "")
        self.__window.ageSpinBox.setValue(user.age if user.age else 0)
        self.__window.genderComboBox.setCurrentText(user.gender or "")
        self.__window.countryComboBox.setCurrentText(user.country or "")
        if user.account_creation_date:
            account_creation_date_str = user.account_creation_date.strftime("%Y-%m-%d")
            self.__window.createdDateEdit.setDate(QDate.fromString(account_creation_date_str, "yyyy-MM-dd"))
        self.set_widget_state(self.__window.lastPurchaseDateEdit, self.__window.dateButton,
                              "Remove date" if user.last_purchase_date else "Add date",
                              bool(user.last_purchase_date))
        if user.last_purchase_date is not None:
            last_purchase_date_str = user.last_purchase_date.strftime("%Y-%m-%d")
            self.__window.lastPurchaseDateEdit.setDate(QDate.fromString(last_purchase_date_str, "yyyy-MM-dd"))
        segment = next((s for s in InitialData.AudienceSegments.get_items() if s.segment_id == user.segment_id), None)
        self.set_widget_state(self.__window.segmentComboBox, self.__window.segmentButton,
                              "Remove segment" if segment else "Add segment",
                              bool(segment))
        if segment is not None:
            self.__window.segmentComboBox.setCurrentText(segment.segment_name)
        else:
            self.__window.segmentComboBox.setCurrentIndex(0)

    def set_segment_name(self, segment_name):
        self.__window.segmentComboBox.setCurrentText(str(segment_name))
        self.__window.segmentComboBox.setEnabled(False)

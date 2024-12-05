
from PyQt5.QtCore import Qt

from Windows import *
from Models import *
import InitialData


class AddAdvertisementWindowController:
    def __init__(self, window):
        self.__window = window

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


    def validate_window(self) -> bool:
        advertisement_topic = self.__window.topicLineEdit.text().strip()
        if not advertisement_topic:
            return False
        return True

    def get_data(self) -> Optional[Advertisement]:
        send_date_qdate = self.__window.sendDateEdit.date()
        campaign_name = self.__window.campaignComboBox.currentText().strip()
        campaign = next((c for c in InitialData.Campaigns.get_items() if c.campaign_name == campaign_name), None)
        platform_name = self.__window.platformComboBox.currentText().strip()
        platform = next((p for p in InitialData.MediaPlatforms.get_items() if p.platform_name == platform_name), None)
        return Advertisement(
            advertisement_id=int(self.__window.idLineEdit.text().strip()),
            text=self.__window.textLineEdit.text().strip(),
            format=self.__window.formatComboBox.currentText(),
            send_time=datetime.combine(send_date_qdate.toPyDate(),
                                        datetime.min.time()) if self.__window.sendDateEdit.isEnabled() else None,
            topic=self.__window.topicLineEdit.text().strip(),
            language=self.__window.languageComboBox.currentText(),
            attachment=self.__window.attachmentLineEdit.text().strip(),
            clicks=int(
                self.__window.clicksLineEdit.text().strip()) if self.__window.clicksLineEdit.text().strip() else None,
            views=int(
                self.__window.viewsLineEdit.text().strip()) if self.__window.viewsLineEdit.text().strip() else None,
            campaign_id=campaign.campaign_id,
            platform_id=platform.platform_id
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

    def set_data(self, advertisement: Advertisement) -> None:
        self.__window.idLineEdit.setText(str(advertisement.advertisement_id))
        self.__window.textLineEdit.setText(advertisement.text or "")
        self.__window.formatComboBox.setCurrentText(advertisement.format or "")
        if advertisement.send_time:
            self.__window.sendDateEdit.setDate(advertisement.send_time)
            self.__window.sendDateEdit.setEnabled(True)
            self.__window.sendDateEdit.setStyleSheet("")
        else:
            self.__window.sendDateEdit.setEnabled(False)
            self.__window.sendDateEdit.setStyleSheet("background-color: lightgray;")
        self.__window.topicLineEdit.setText(advertisement.topic or "")
        self.__window.languageComboBox.setCurrentText(advertisement.language or "")
        self.__window.attachmentLineEdit.setText(advertisement.attachment or "")
        self.__window.clicksLineEdit.setText(str(advertisement.clicks) if advertisement.clicks is not None else "")
        self.__window.viewsLineEdit.setText(str(advertisement.views) if advertisement.views is not None else "")
        campaign = next((c for c in InitialData.Campaigns.get_items() if c.campaign_id == advertisement.campaign_id), None)
        if campaign:
            self.__window.campaignComboBox.setCurrentText(campaign.campaign_name)
        else:
            self.__window.campaignComboBox.setCurrentText("")
        platform = next((p for p in InitialData.MediaPlatforms.get_items() if p.platform_id == advertisement.platform_id),
                        None)
        if platform:
            self.__window.platformComboBox.setCurrentText(platform.platform_name)
        else:
            self.__window.platformComboBox.setCurrentText("")

    def set_campaign_name(self, campaign_name):
        self.__window.campaignComboBox.setCurrentText(str(campaign_name))
        self.__window.campaignComboBox.setEnabled(False)

    def set_platform_name(self, platform_name):
        self.__window.platformComboBox.setCurrentText(str(platform_name))
        self.__window.platformComboBox.setEnabled(False)


class AddCampaignWindowController:
    def __init__(self, window):
        self.__window = window

    def select_max_id_from_table(self) -> int:
        if not InitialData.Campaigns.get_items():
            return -1
        try:
            max_id = max(c.campaign_id for c in InitialData.Campaigns.get_items())
            return max_id
        except ValueError:
            return -1

    def validate_window(self) -> bool:
        campaign_goal = self.__window.goalLineEdit.text().strip()
        if not campaign_goal:
            return False
        return True

    def get_data(self) -> Optional[Campaign]:
        start_date_qdate = self.__window.startDateEdit.date()
        end_date_qdate = self.__window.endDateEdit.date()

        return Campaign(
            campaign_id=int(self.__window.idLineEdit.text().strip()),
            campaign_name=self.__window.nameLineEdit.text().strip(),
            start_date=datetime.combine(start_date_qdate.toPyDate(), datetime.min.time()) if self.__window.startDateEdit.isEnabled() else None,
            end_date=datetime.combine(end_date_qdate.toPyDate(), datetime.min.time()) if self.__window.endDateEdit.isEnabled() else None,
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
        self.__window.startDateEdit.setEnabled(True)
        self.__window.endDateEdit.setEnabled(True)
        self.__window.budgetSpinBox.setEnabled(True)
        self.__window.goalLineEdit.clear()
        self.__window.budgetSpinBox.setValue(1000)
        self.__window.companyComboBox.setCurrentIndex(0)

    def set_data(self, campaign: Campaign) -> None:
        print(campaign.start_date)
        print(type(campaign.start_date))
        self.__window.idLineEdit.setText(str(campaign.campaign_id))
        self.__window.nameLineEdit.setText(campaign.campaign_name or "")
        if campaign.start_date:
            self.__window.startDateEdit.setDate(campaign.start_date)
            self.__window.startDateEdit.setEnabled(True)
            self.__window.startDateEdit.setStyleSheet("")
        else:
            self.__window.startDateEdit.setEnabled(False)
            self.__window.startDateEdit.setStyleSheet("background-color: lightgray;")

        if campaign.end_date:
            self.__window.endDateEdit.setDate(campaign.end_date)
            self.__window.endDateEdit.setEnabled(True)
            self.__window.endDateEdit.setStyleSheet("")
        else:
            self.__window.endDateEdit.setEnabled(False)
            self.__window.endDateEdit.setStyleSheet("background-color: lightgray;")

        if campaign.budget is not None:
            self.__window.budgetSpinBox.setValue(campaign.budget)
            self.__window.budgetSpinBox.setEnabled(True)
            self.__window.budgetSpinBox.setStyleSheet("")
        else:
            self.__window.budgetSpinBox.setEnabled(False)
            self.__window.budgetSpinBox.setStyleSheet("background-color: lightgray;")

        self.__window.goalLineEdit.setText(campaign.goal or "")
        self.__window.companyComboBox.setCurrentText(campaign.company_name or "")




class AddClientWindowController:
    def __init__(self, window):
        self.__window = window

    def validate_window(self) -> bool:
        client_name = self.__window.nameLineEdit.text().strip()
        client_phone = self.__window.phoneLineEdit.text().strip()
        client_email = self.__window.emailLineEdit.text().strip()
        client_password = self.__window.passwordLineEdit.text().strip()
        if not client_name or not client_phone or not client_email or not client_password:
            return False
        return True

    def get_data(self) -> Optional[Client]:

        return Client(
            company_name=self.__window.nameLineEdit.text().strip(),
            phone=self.__window.phoneLineEdit.text().strip(),
            email=self.__window.emailLineEdit.text().strip(),
            password=self.__window.passwordLineEdit.text().strip(),
            address=self.__window.addressLineEdit.text().strip(),
            type=self.__window.typeComboBox.currentText(),
            business_area=self.__window.areaComboBox.currentText(),
            available_budget=self.__window.budgetSpinBox.value()
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

    def set_data(self, client) -> None:
        self.__window.nameLineEdit.setText(client.company_name or "")
        self.__window.phoneLineEdit.setText(client.phone or "")
        self.__window.emailLineEdit.setText(client.email or "")
        self.__window.passwordLineEdit.setText(client.password or "")
        self.__window.addressLineEdit.setText(client.address or "")
        self.__window.typeComboBox.setCurrentText(client.type or "")
        self.__window.areaComboBox.setCurrentText(client.business_area or "")
        self.__window.budgetSpinBox.setValue(client.available_budget or 0)


class TablesWindowController:
    def __init__(self, window):
        self.__window = window
        self.current_data = InitialData.Clients

    def fill_table(self, data) -> None:
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
            related_data_map[header]["new_header"] if header in related_data_map else header
            for header in headers
        ]
        self.__window.dataTableWidget.setRowCount(len(data))
        self.__window.dataTableWidget.setColumnCount(len(headers))
        self.__window.dataTableWidget.setHorizontalHeaderLabels(updated_headers)
        for row_ind, row_data in enumerate(data.get_items()):
            for col_ind, col_data in enumerate(row_data.GetData()[1]):
                if col_data:
                    header_name = headers[col_ind]
                    if header_name in related_data_map and col_data in related_data_map[header_name]["map"]:
                        display_value = related_data_map[header_name]["map"][col_data]
                    else:
                        display_value = str(col_data)
                    item = QTableWidgetItem(display_value)
                else:
                    item = QTableWidgetItem("")
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.__window.dataTableWidget.setItem(row_ind, col_ind, item)

    def update_table(self, data) -> None:
        self.fill_table(data)
        self.__window.databaseNameLabel.setText(data.get_str_models_name())
        self.current_data = data

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
        remove_item = next(
            (item for item in self.current_data.get_items() if str(item.GetData()[1][0]) == key_value),
            None
        )
        if remove_item:
            self.current_data.remove(remove_item)
            return key_value
        return None

    def get_item_for_edit(self, selected_row: int) -> Optional[Any]:
        if selected_row == -1:
            return None

        return self.current_data.get_items()[selected_row]

    def save_item(self, data: Any, edit: bool, selected_row: Optional[int] = None) -> None:


        if edit and selected_row is not None:
            self.current_data.update(selected_row, data)
        else:
            self.current_data.add(data)


class AddPlatformWindowController:
    def __init__(self, window):
        self.__window = window

    def validate_window(self) -> bool:
        platform_name = self.__window.nameLineEdit.text().strip()
        if not platform_name:
            return False
        return True

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
            platform_type=self.__window.typeComboBox.currentText().strip(),
            main_ad_format=self.__window.formatComboBox.currentText().strip(),
            audience_size=int(self.__window.audienceSpinBox.value()) if self.__window.audienceSpinBox.value() else None
        )

    def reset_data(self):
        max_id = self.select_max_id_from_table()
        self.__window.idLineEdit.setText(str(max_id + 1))
        self.__window.nameLineEdit.clear()
        self.__window.typeComboBox.setCurrentIndex(0)
        self.__window.formatComboBox.setCurrentIndex(0)
        self.__window.audienceSpinBox.setValue(0)

    def set_data(self, platform: MediaPlatform) -> None:
        self.__window.idLineEdit.setText(str(platform.platform_id))
        self.__window.nameLineEdit.setText(platform.platform_name or "")
        self.__window.typeComboBox.setCurrentText(platform.platform_type or "")
        self.__window.formatComboBox.setCurrentText(platform.main_ad_format or "")
        self.__window.audienceSpinBox.setValue(platform.audience_size if platform.audience_size is not None else 0)


class AddSegmentWindowController:
    def __init__(self, window):
        self.__window = window

    def validate_window(self) -> bool:
        minimum_age = self.__window.minimumSpinBox.value()
        maximum_age = self.__window.maximumSpinBox.value()
        gender = self.__window.genderComboBox.currentText().strip()
        language = self.__window.languageComboBox.currentText().strip()
        if not minimum_age or not maximum_age or not gender or not language:
            return False
        return True

    def select_max_id_from_table(self) -> int:

        if not InitialData.AudienceSegments.get_items():
            return -1
        try:
            max_id = max(s.segment_id for s in InitialData.AudienceSegments.get_items())
            return max_id
        except ValueError:
            return -1

    def get_data(self):

        return AudienceSegment(
            segment_id=int(self.__window.idLineEdit.text().strip()),
            segment_name=self.__window.nameLineEdit.text().strip() if self.__window.nameLineEdit.text().strip() else None,
            age_range=f"{self.__window.minimumSpinBox.value()}-{self.__window.maximumSpinBox.value()}",
            gender=self.__window.genderComboBox.currentText().strip(),
            location=self.__window.locationComboBox.currentText().strip() if self.__window.locationComboBox.currentIndex() != 0 else None,
            general_interest=self.__window.interestLineEdit.text().strip() if self.__window.interestLineEdit.text().strip() else None,
            socioeconomic_status=self.__window.statusLineEdit.text().strip() if self.__window.statusLineEdit.text().strip() else None,
            language=self.__window.languageComboBox.currentText().strip(),
            behavioral_characteristics=self.__window.characteristicsLineEdit.text().strip() if self.__window.characteristicsLineEdit.text().strip() else None,
            device_used=self.__window.deviceComboBox.currentText().strip() if self.__window.deviceComboBox.currentIndex() != 0 else None,
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

    def set_data(self, segment: AudienceSegment) -> None:
        self.__window.idLineEdit.setText(str(segment.segment_id))
        self.__window.nameLineEdit.setText(segment.segment_name or "")
        self.__window.minimumSpinBox.setValue(int(segment.age_range[:2]))
        self.__window.maximumSpinBox.setValue(int(segment.age_range[3:]))
        self.__window.genderComboBox.setCurrentText(segment.gender or "")
        self.__window.locationComboBox.setCurrentText(segment.location or "")
        self.__window.languageComboBox.setCurrentText(segment.language or "")
        self.__window.deviceComboBox.setCurrentText(segment.device_used or "")
        self.__window.interestLineEdit.setText(segment.general_interest or "")
        self.__window.statusLineEdit.setText(segment.socioeconomic_status or "")
        self.__window.characteristicsLineEdit.setText(segment.behavioral_characteristics or "")

class AddUserWindowController:
    def __init__(self, window):
        self.__window = window

    def validate_window(self) -> bool:
        email = self.__window.emailLineEdit.text().strip()
        password = self.__window.passwordLineEdit.text().strip()
        age = self.__window.ageSpinBox.value()
        gender = self.__window.genderComboBox.currentText().strip()
        country = self.__window.countryComboBox.currentText().strip()
        account_creation_date = self.__window.createdDateEdit.text().strip()
        if not email or not password or not age or not gender or not country or not account_creation_date:
            return False
        return True

    def get_data(self) -> Optional[User]:
        segment_name = self.__window.segmentComboBox.currentText().strip()
        segment = next((s for s in InitialData.AudienceSegments.get_items() if s.segment_name == segment_name), None)
        return User(
            email=self.__window.emailLineEdit.text().strip(),
            password=self.__window.passwordLineEdit.text().strip(),
            age=int(self.__window.ageSpinBox.value()),
            gender=self.__window.genderComboBox.currentText().strip(),
            country=self.__window.countryComboBox.currentText().strip(),
            account_creation_date=self.__window.createdDateEdit.date().toString("yyyy-MM-dd"),
            last_purchase_date=self.__window.lastPurchaseDateEdit.date().toString("yyyy-MM-dd") if self.__window.lastPurchaseDateEdit.text().strip() else None,
            segment_id=segment.segment_id if segment else None,
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

    def set_data(self, user: User) -> None:
        self.__window.emailLineEdit.setText(user.email or "")
        self.__window.passwordLineEdit.setText(user.password or "")
        self.__window.ageSpinBox.setValue(user.age if user.age else 0)
        self.__window.genderComboBox.setCurrentText(user.gender or "")
        self.__window.countryComboBox.setCurrentText(user.country or "")
        if user.account_creation_date:
            account_creation_date_str = user.account_creation_date.strftime("%Y-%m-%d")
            self.__window.createdDateEdit.setDate(QDate.fromString(account_creation_date_str, "yyyy-MM-dd"))
        if user.last_purchase_date:
            last_purchase_date_str = user.last_purchase_date.strftime("%Y-%m-%d")
            self.__window.lastPurchaseDateEdit.setDate(QDate.fromString(last_purchase_date_str, "yyyy-MM-dd"))
        else:
            self.__window.lastPurchaseDateEdit.clear()

        segment = next((s for s in InitialData.AudienceSegments.get_items() if s.segment_id == user.segment_id), None)
        if segment:
            self.__window.segmentComboBox.setCurrentText(segment.segment_name)
        else:
            self.__window.segmentComboBox.setCurrentIndex(0)



from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve

from crud.views import UdsMetaAprHTMxTableView, UdsMetaHTMxTableView, history_views, profile, bascet, get_html_apr, get_html_uds, password_change, logout

from grr.views import UdsMetaGrrAccomHTMxTableView, UdsMetaGrrStageHTMxTableView, get_html_grr_stage
class TestUrls(SimpleTestCase):
    
    def test_history_urls_is_resolved(self):
        url = reverse('crud:history')
        self.assertEquals(resolve(url).func, history_views)
        
    def test_uds_meta_apr_urls_is_resolved(self):
        url = reverse('crud:table_apr')
        self.assertEquals(resolve(url).func.view_class, UdsMetaAprHTMxTableView)
        
    def test_profile_urls_is_resolved(self):
        url = reverse('crud:profile')
        self.assertEquals(resolve(url).func, profile)
        
    def test_bascet_urls_is_resolved(self):
        url = reverse('crud:bascet')
        self.assertEquals(resolve(url).func, bascet)
    
    def test_uds_meta_urls_is_resolved(self):
        url = reverse('crud:table')
        self.assertEquals(resolve(url).func.view_class, UdsMetaHTMxTableView)
        
    def test_get_html_apr_urls_is_resolved(self):
        url = reverse('crud:get_html_apr')
        self.assertEquals(resolve(url).func, get_html_apr)
    
    def test_get_html_uds_urls_is_resolved(self):
        url = reverse('crud:get_html_uds')
        self.assertEquals(resolve(url).func, get_html_uds)
        
    def test_logout_urls_is_resolved(self):
        url = reverse('crud:logout')
        self.assertEquals(resolve(url).func, logout)
    
    def test_password_change_urls_is_resolved(self):
        url = reverse('crud:password_change')
        self.assertEquals(resolve(url).func, password_change)
        
    def test_grr_accom_urls_is_resolved(self):
        url = reverse('grr:grr_accom')
        self.assertEquals(resolve(url).func.view_class, UdsMetaGrrAccomHTMxTableView)
           
    def test_grr_stage_urls_is_resolved(self):
        url = reverse('grr:grr_stage')
        self.assertEquals(resolve(url).func.view_class, UdsMetaGrrStageHTMxTableView)
        
    def test_get_html_grr_urls_is_resolved(self):
        url = reverse('grr:get_html_grr')
        self.assertEquals(resolve(url).func, get_html_grr_stage)

# class TestDb(TestCase):

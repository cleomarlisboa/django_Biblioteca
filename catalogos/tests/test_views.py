from django.test import TestCase
from django.urls import reverse

from catalogos.models import Autor

class AutorListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        autoresQtd = 13

        for autor_id in range(autoresQtd):
            Autor.objects.create(
                nome='Machado',
                sobrenome='Assis',
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/catalogos/autores/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('autores'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('autores'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalogos/autor_list.html')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('autores'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['autor_list']) == 10)

    def test_lists_all_autores(self):
        response = self.client.get(reverse('autores')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['autor_list']) == 3)

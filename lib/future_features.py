#
# Autor: Matias Novoa
# Año: 2014
# Licencia: GNU/GPL V3 http://www.gnu.org/copyleft/gpl.html
#

class ImprimirScreen(Screen):

    def __init__(self, name=''):
        '''Pantalla para imprimir los tickets del usuario'''
        self.data = {}
        self.name = name
        self.cargar_datos()
        self.mensaje = StringProperty("")
        Screen.__init__(self)

    def confirmacion(self, row):
        if self.data[row]['estado'] == 'Activo':
            content = ConfirmPopup(text='Seguro deseas imprimir?')
            content.bind(on_answer=self._on_answer)
            self.popup = Popup(title="Advertencia",
                                    content=content,
                                    size_hint=(None, None),
                                    size=(400,400),
                                    auto_dismiss= False)
            self.row = row
            self.popup.open()

    def _on_answer(self, instance, answer):
        if answer:
            self.imprimir_ticket()
        self.popup.dismiss()

    def check_hora(self, fecha, hora=11):
        '''Verifica que no se pueda imprimir un ticket despues de la hora'''
        ahora = datetime.now()
        fecha = datetime.strptime(fecha, '%d/%m/%Y')
        if fecha.year == ahora.year:
            if fecha.month == ahora.month and fecha.day == ahora.day:
                if ahora.hour >= hora:
                    return False
                else:
                    return True
            else:
                return True
        else:
            return True

    def imprimir_ticket(self):
        '''Imprime el ticket de la fila row.'''
        row = self.row
        fecha = self.data[row]['fecha']
        id_ticket = self.data[row]['id']
        code = self.data[row]['barcode']
        band = self.check_hora(fecha, 14)
        if id_ticket and band:
            nom = self.data['nombre']
            dni = self.data['dni']
            cat = self.data['categoria']
            fac = self.data['facultad']
            unit = '03'
            ticket = str(id_ticket)
            print_thread = Thread(target=impresora.imprimir_ticket_alumno,
                        args=(nom, dni, fac, cat, code, unit, ticket, fecha))
            print_thread.start()
            controlador.insert_log(self.user, 'imprimir')
        else:
            if not id_ticket:
                self.mensaje = "No puede imprimir un ticket anulado."
            elif not band:
                self.mensaje = "No puede imprimir un ticket despues\r\n de las 14 hs. del día de servicio."
            WarningPopup().open()

    def update_datos(self):
        '''Actualiza los datos de la pantalla para plasmar cambios'''
        user_session.update(controlador.get_usuario(self.data['dni']))
        self.cargar_datos()
        self.ids.saldo.text = self.data['saldo']
        self.ids.nombre.text = self.data['nombre']

    def cargar_datos(self):
        '''Carga los datos del usuario dentro de la pantalla de impresión'''
        self.user = user_session.get_user()
        self.data['nombre'] = self.user['nombre']
        self.data['dni'] = self.user['dni']
        self.data['saldo'] = '$%.2f' % (self.user['saldo'])
        self.data['categoria'] = controlador.get_categoria_nombre(self.user['id_categoria'])
        self.data['facultad'] = controlador.get_facultad(self.user['id_facultad'])
        self.data['ruta_foto'] = self.user['ruta_foto']
        self.cargar_tickets()
        
    def cargar_tickets(self): 
        '''
        Carga los próximos 2 tickets en la pantalla, solo se actualiza
        en caso salir y volver a entrar'''   
        self.tickets = controlador.get_tickets(self.user, 2)
        ticket_vacio = {'fecha': '', 'importe': '', 'estado': '', 'id': 0,
                        'barcode': ''}
        i = 0
        for ticket in self.tickets:
            if ticket['estado']:
                ticket['estado'] = 'Activo'
            else:
                ticket['estado'] = 'Anulado'
            ticket['importe'] = '$%.2f' %(ticket['importe'])
            ticket['fecha'] = ticket['fecha'].strftime('%d/%m/%Y')
            self.data['rows%s' % (i)] = ticket
            i += 1
        faltantes = 2 - len(self.tickets)
        if faltantes:
            if faltantes == 1:
                self.data['rows1'] = ticket_vacio
            else:
                self.data['rows0'] = ticket_vacio
                self.data['rows1'] = ticket_vacio
            
    def cancel(self):
        '''Vuelve a una pantalla anterior'''
        self.manager.current = 'menu'


class Compra4Screen(Screen):

    def __init__(self, dias, name=''):
        '''Pantalla para imprimir los tickets del usuario'''
        self.data = {}
        self.name = name
        self.dias = dias
        self.cargar_datos()
        self.mensaje = StringProperty("")
        Screen.__init__(self)

    def update_datos(self):
        '''Actualiza los datos de la pantalla para plasmar cambios'''
        user_session.update(controlador.get_usuario(self.data['dni']))
        self.cargar_datos()
        self.ids.saldo.text = self.data['saldo']
        self.ids.nombre.text = self.data['nombre']

    def cargar_datos(self):
        '''Carga los datos del usuario dentro de la pantalla de compra'''
        self.user = user_session.get_user()
        self.data['nombre'] = self.user['nombre']
        self.data['dni'] = self.user['dni']
        self.data['saldo'] = '$%.2f' % (self.user['saldo'])
        self.data['categoria'] = controlador.get_categoria_nombre(self.user['id_categoria'])
        self.data['facultad'] = controlador.get_facultad(self.user['id_facultad'])
        self.data['ruta_foto'] = self.user['ruta_foto']

    def check_hora(self, fecha, hora=11):
        '''Verifica que no se pueda comprar/imprimir un ticket despues de hora'''
        ahora = datetime.now()
        fecha = datetime.strptime(fecha, '%d/%m/%Y')
        if fecha.year == ahora.year:
            if fecha.month == ahora.month and fecha.day == ahora.day:
                if ahora.hour >= hora:
                    return False
                else:
                    return True
            else:
                return True
        else:
            return True

    def imprimir_primero(self):
        row = controlador.get_ticket(self.user, self.dias[0])
        id_ticket = row['id']
        fecha = row['fecha'].strftime('%d/%m/%Y')
        code = row['barcode']
        band = self.check_hora(fecha, 14)
        if band:
            nom = self.data['nombre']
            dni = self.data['dni']
            cat = self.data['categoria']
            fac = self.data['facultad']
            unit = '03' # chequear db TODO
            ticket = str(id_ticket)
            print_thread = Thread(target=impresora.imprimir_ticket_alumno,
                        args=(nom, dni, fac, cat, code, unit, ticket, fecha))
            print_thread.start()
            controlador.insert_log(self.user, 'imprimir')
        else:
            self.mensaje = "No puede imprimir un ticket despues\r\n de las 14 hs. del día de servicio."
            WarningPopup().open()
        self.cancel()

    def imprimir_todos(self):
        for dia in self.dias:
            row = controlador.get_ticket(self.user, dia)
            id_ticket = row['id']
            fecha = row['fecha'].strftime('%d/%m/%Y')
            code = row['barcode']
            band = self.check_hora(fecha, 14)
            if band:
                nom = self.data['nombre']
                dni = self.data['dni']
                cat = self.data['categoria']
                fac = self.data['facultad']
                unit = '03' # chequear db TODO
                ticket = str(id_ticket)
                print_thread = Thread(target=impresora.imprimir_ticket_alumno,
                        args=(nom, dni, fac, cat, code, unit, ticket, fecha))
                print_thread.start()
                controlador.insert_log(self.user, 'imprimir')
            else:
                self.mensaje = "No puede imprimir un ticket despues\r\n de las 14 hs. del día de servicio."
                WarningPopup().open()
        self.cancel()

    def cancel(self):
        '''Vuelve a una pantalla anterior'''
        self.manager.current = 'menu'
        self.manager.remove_widget(self.manager.get_screen('compra_1'))
        self.manager.remove_widget(self.manager.get_screen('compra_2'))
        self.manager.remove_widget(self.manager.get_screen('compra_4'))

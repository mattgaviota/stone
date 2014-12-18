<div class="container">
	<div class="row page-header">
		<script type="text/javascript">
			base_url = '<?=base_url(); ?>';
		</script>
		<script src="<?= base_url('js/control-tickets.js'); ?>"></script>
		<div class="col-md-4">
			<div id="barcode" class="mijumbotron">
				<legend>Código de Barra</legend>
				<fieldset>
					<div class="form-group">
						<label for="barcode">Código de Barra</label>
						<input id="barcode" type="text" name="barcode" class="form-control">
						<hr>
						<button id="enviar-barcode" type="submit" class="btn btn-primary boton-grande">Enviar</button>
						
					</div>				
				</fieldset>
			</div>
		</div>

		<div class="col-md-4">
			<div class="mijumbotron">
				<legend>Información del Usuario</legend>
				<fieldset>
				<div id="info-usuario">
					
				</div>
				</fieldset>
			</div>
		</div>

		<div class="col-md-4">
			<div class="mijumbotron">
				<legend>Información del Ticket</legend>
				<fieldset>
				<div id="info-ticket">
					
				</div>
				</fieldset>
			</div>
		</div>

	</div>
</div>
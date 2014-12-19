<div class="row">
	<h3>Informes Estadísticos</h3>
	<div role="tabpanel">
		<!-- Nav tabs -->
		<ul class="nav nav-tabs" role="tablist">
		<li role="presentation" class="active"><a href="#informe1" aria-controls="informe1" role="tab" data-toggle="tab">Clasificación de Usuarios</a></li>
		<li role="presentation"><a href="#informe2" aria-controls="informe2" role="tab" data-toggle="tab">Servicios por Facultad</a></li>
		<li role="presentation"><a href="#informe3" aria-controls="informe3" role="tab" data-toggle="tab">Clasificación de Tickets</a></li>
		</ul>

		
		<div class="tab-content">
			<!-- Tabla para el primer reporte -->
			<div role="tabpanel" class="tab-pane active" id="informe1">
				<br>
				<table class="table table-bordered table-striped table-hover">
					<thead>
						<tr>
							<th> Facultades </th>
							<th> Total de Usuarios </th>
							<th> Becados </th>
							<th> Regulares </th>
							<th> Gratuitos </th>
						</tr>
					</thead>

					<tbody>
						<?php foreach ($registros as $registro): ?>
						<tr>
							<td><?= $registro->facultad; ?></td>
							<td><?= $registro->total_usuarios; ?></td>
							<td><?= $registro->becados; ?></td>
							<td><?= $registro->regulares; ?></td>
							<td><?= $registro->gratuitos; ?></td>
						</tr>
						<?php endforeach; ?>
						<tr class="info">
							<td>Totales: </td>
							<td><?= $totales->total_usuarios; ?></td>
							<td><?= $totales->becados; ?></td>
							<td><?= $totales->regulares; ?></td>
							<td><?= $totales->gratuitos; ?></td>
						</tr>
					</tbody>
				</table>
				<div class="col-md-offset-9">
					<?= form_open('index.php/reportes/generar_pdf'); ?>
						<input type="submit" class="btn btn-primary glyphicon glyphicon-print" value=" Descargar PDF" name="PDF1">
					<?= form_close(); ?>
				</div>
			</div>
			<!-- Tabla para el segundo reporte -->
			<div role="tabpanel" class="tab-pane" id="informe2">
				<br>
				<div class="filtros">
					<fieldset>
						<?= form_open('index.php/reportes/generar_pdf', array('id'=>'form_reporte')); ?>
						<div class="row">
							<div class="form-group">
								<div class="col-md-6">
									<label for="radio_dia">Por Día</label>&nbsp;
									<input type="radio" id="radio_dia" name="filtro_radio" value="filtrodia" checked="checked">&nbsp;
									<label for="radio_intervalo">Por intervalo</label>&nbsp;	
									<input type="radio" id="radio_intervalo" name="filtro_radio" value="filtrointervalo">
								</div>
							</div>
						</div>

						<br>
						
						<div class="row filtro filtrodia">
							<div class="form-group">
								<label for="dia" class="col-md-2">Por Día: </label>
								<div class="col-md-4">
									<input id="dia" name="dia" type="text" class="form-control" value="<?= $desde; ?>"/>
								</div>
								<div class="col-md-4">
									<button type="button" class="btn btn-primary boton-filtrar glyphicon glyphicon-leaf"> Filtrar</button>
								</div>
							</div>
							
						</div>
						
						<div class="filtro filtrointervalo">
							<div class="row">
								<div class="form-group">
									<label for="desde" class="col-md-2">Desde: </label>
									<div class="col-md-4">
										<input id="desde" name="desde" type="text" class="form-control" />
									</div>	
								</div>
							</div>

							<br>

							<div class="row">
								<div class="form-group">
									<label for="hasta" class="col-md-2">Hasta: </label>
									<div class="col-md-4">
										<input id="hasta" name="hasta" type="text" class="form-control" />
									</div>
									<div class="col-md-4">
										<button type="button" class="btn btn-primary boton-filtrar glyphicon glyphicon-leaf"> Filtrar</button>	
									</div>	
								</div>
							</div>
						</div>
						<?= form_close(); ?>
					</fieldset>
				</div>

				<br>
				
				<table class="table table-bordered table-striped table-hover">
					<thead>
						<tr>
							<th> Facultades </th>
							<th> Tickets Consumidos </th>
							<th> Becados </th>
							<th> Regulares </th>
							<th> Gratuitos </th>
							<th> Total en $ </th>
						</tr>
					</thead>
					<tbody id="resultado_tickets_tabla">
						<?php foreach ($registros2 as $registro2): ?>
						<tr>
							<td><?= $registro2->facultad; ?></td>
							<td><?= $registro2->total_tickets; ?></td>
							<td><?= $registro2->becados; ?></td>
							<td><?= $registro2->regulares; ?></td>
							<td><?= $registro2->gratuitos; ?></td>
							<td><?= $registro2->total_pesos; ?></td>
						</tr>
						<?php endforeach; ?>
						<tr class="info">
							<td>Totales: </td>
							<td><?= $totales2->total_tickets; ?></td>
							<td><?= $totales2->becados; ?></td>
							<td><?= $totales2->regulares; ?></td>
							<td><?= $totales2->gratuitos; ?></td>
							<td><?= $totales2->total_importe; ?></td>
						</tr>
					</tbody>
				</table>
				<div class="col-md-offset-9">
					<input form="form_reporte" type="submit" class="btn btn-primary glyphicon glyphicon-print" value=" Descargar PDF" name="PDF2">
				</div>
			</div>

			<!-- Tabla para el tercer reporte -->
			<div role="tabpanel" class="tab-pane" id="informe3">
				<br>
				<div class="filtros">
					<fieldset>
						<?= form_open('index.php/reportes/generar_pdf', array('id'=>'form_reporte2')); ?>
						<div class="row">
							<div class="form-group">
								<div class="col-md-6">
									<label for="radio_dia2">Por Día</label>&nbsp;
									<input type="radio" id="radio_dia2" name="filtro_radio2" value="filtrodia2" checked="checked">&nbsp;
									<label for="radio_intervalo2">Por intervalo</label>&nbsp;	
									<input type="radio" id="radio_intervalo" name="filtro_radio2" value="filtrointervalo2">
								</div>
							</div>
						</div>

						<br>
						
						<div class="row filtro2 filtrodia2">
							<div class="form-group">
								<label for="dia2" class="col-md-2">Por Día: </label>
								<div class="col-md-4">
									<input id="dia2" name="dia2" type="text" class="form-control" value="<?= $desde; ?>"/>
								</div>
								<div class="col-md-4">
									<button type="button" class="btn btn-primary boton-filtrar2 glyphicon glyphicon-leaf"> Filtrar</button>
								</div>
							</div>
						</div>
						
						<div class="filtro2 filtrointervalo2">
							<div class="row">
								<div class="form-group">
									<label for="desde2" class="col-md-2">Desde: </label>
									<div class="col-md-4">
										<input id="desde2" name="desde2" type="text" class="form-control" />
									</div>
								</div>
							</div>

							<br>

							<div class="row">
								<div class="form-group">
									<label for="hasta2" class="col-md-2">Hasta: </label>
									<div class="col-md-4">
										<input id="hasta2" name="hasta2" type="text" class="form-control" />
									</div>
									<div class="col-md-4">
										<button type="button" class="btn btn-primary boton-filtrar2 glyphicon glyphicon-leaf"> Filtrar</button>
									</div>	
								</div>
							</div>
						</div>
						<?= form_close(); ?>
					</fieldset>
				</div>

				<br>

				<table class="table table-bordered table-striped table-hover">
					<thead>
						<tr>
							<th> Facultades </th>
							<th> Total de Tickets </th>
							<th> Anulados </th>
							<th> Activos </th>
							<th> Impresos </th>
							<th> Consumidos </th>
						</tr>
					</thead>
					<tbody id="resultado_tickets_tabla2">
						<?php foreach ($registros3 as $registro3): ?>
						<tr>
							<td><?= $registro3->facultad; ?></td>
							<td><?= $registro3->total_tickets; ?></td>
							<td><?= $registro3->anulados; ?></td>
							<td><?= $registro3->activos; ?></td>
							<td><?= $registro3->impresos; ?></td>
							<td><?= $registro3->consumidos; ?></td>
						</tr>
						<?php endforeach; ?>
						<tr class="info">
							<td>Totales: </td>
							<td><?= $totales3->total_tickets; ?></td>
							<td><?= $totales3->anulados; ?></td>
							<td><?= $totales3->activos; ?></td>
							<td><?= $totales3->impresos; ?></td>
							<td><?= $totales3->consumidos; ?></td>
						</tr>
					</tbody>
				</table>
				<div class="col-md-offset-9">
					<input form="form_reporte2" type="submit" class="btn btn-primary glyphicon glyphicon-download" value=" Descargar PDF" name="PDF3">
				</div>
			</div>
		</div>
	</div>	
</div>
<script type="text/javascript">
	base_url = '<?=base_url(); ?>';
</script>
<script src="<?= base_url('js/reportes.js'); ?>"></script>
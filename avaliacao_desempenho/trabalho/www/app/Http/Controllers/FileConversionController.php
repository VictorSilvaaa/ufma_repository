<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use PhpOffice\PhpWord\IOFactory;
use PhpOffice\PhpWord\Settings;

class FileConversionController extends Controller
{
    public function store(Request $request)
    {
        // Validação do arquivo recebido
        $request->validate([
            'file' => 'required|file|mimes:docx|max:10240',
        ]);

        // Obter o arquivo enviado
        $file = $request->file('file');
        $fileName = time() . '.' . $file->extension();
        $file->move(public_path('uploads'), $fileName);

        // Configurar o DomPDF como renderizador para PHPWord
        $domPdfPath = base_path('vendor/dompdf/dompdf');
        Settings::setPdfRendererPath($domPdfPath);
        Settings::setPdfRendererName('DomPDF');

        try {
            // Ler o arquivo .docx e criar o PDF
            $content = IOFactory::load(public_path('uploads/' . $fileName));
            $pdfWriter = IOFactory::createWriter($content, 'PDF');

            $pdfFileName = time() . '.pdf';
            $pdfWriter->save(public_path('uploads/' . $pdfFileName));

            // Retornar o PDF gerado como resposta
            return response()->download(public_path('uploads/' . $pdfFileName));
        } catch (\Exception $e) {
            return response()->json([
                'error' => 'Erro ao converter o arquivo: ' . $e->getMessage(),
            ], 500);
        }
    }
}

package com.esgnexus.service;

import com.esgnexus.domain.ConfiguracaoSistema;
import com.esgnexus.dto.ConfiguracaoDtos;
import com.esgnexus.repository.ConfiguracaoSistemaRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class ConfiguracaoService {
    private final ConfiguracaoSistemaRepository repository;

    public List<ConfiguracaoDtos.ConfiguracaoResponse> listar() {
        return repository.findAll().stream().map(s -> new ConfiguracaoDtos.ConfiguracaoResponse(s.getId(), s.getChave(), s.getValor())).toList();
    }

    public ConfiguracaoDtos.ConfiguracaoResponse salvarOuAtualizar(ConfiguracaoDtos.ConfiguracaoRequest request) {
        ConfiguracaoSistema entity = repository.findByChave(request.chave())
                .orElse(ConfiguracaoSistema.builder().chave(request.chave()).build());
        entity.setValor(request.valor());
        ConfiguracaoSistema saved = repository.save(entity);
        return new ConfiguracaoDtos.ConfiguracaoResponse(saved.getId(), saved.getChave(), saved.getValor());
    }

    public double obterPeso(String chave, double valorPadrao) {
        return repository.findByChave(chave)
                .map(s -> Double.parseDouble(s.getValor()))
                .orElse(valorPadrao);
    }
}

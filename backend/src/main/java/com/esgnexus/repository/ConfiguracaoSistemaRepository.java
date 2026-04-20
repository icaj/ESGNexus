package com.esgnexus.repository;

import com.esgnexus.domain.ConfiguracaoSistema;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface ConfiguracaoSistemaRepository extends JpaRepository<ConfiguracaoSistema, Long> {
    Optional<ConfiguracaoSistema> findByChave(String chave);
}

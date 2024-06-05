package si.primerjanjeCen.nepremicnine.dao;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;
import si.primerjanjeCen.nepremicnine.vao.Nepremicnina;

import java.util.List;

public interface NepremicninaRepository extends MongoRepository<Nepremicnina, String> {
    List<Nepremicnina> findByIdIn(List<String> ids);

}
